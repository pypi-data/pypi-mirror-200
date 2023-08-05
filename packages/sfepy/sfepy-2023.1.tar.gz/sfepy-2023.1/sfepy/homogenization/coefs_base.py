from __future__ import absolute_import
import os

import numpy as nm
import scipy as sc
from collections.abc import Iterable

from sfepy.base.base import output, assert_, get_default, debug, Struct
from sfepy.base.timing import Timer
from sfepy.discrete.evaluate import eval_equations
from sfepy.solvers.ts import TimeStepper
from sfepy.solvers import Solver, eig
from sfepy.linalg import MatrixAction
from .utils import iter_sym, iter_nonsym, create_pis, create_scalar_pis,\
    rm_multi
import six
from six.moves import range

class MiniAppBase(Struct):
    def any_from_conf(name, problem, kwargs):
        try:
            cls = kwargs['class']
        except KeyError:
            raise KeyError("set 'class' for MiniApp %s!" % name)
        obj = cls(name, problem, kwargs)
        return obj
    any_from_conf = staticmethod(any_from_conf)

    def __init__(self, name, problem, kwargs):
        Struct.__init__(self, name=name, problem=problem, **kwargs)

        if self.problem is not None:
            self.problem.clear_equations()

        self.set_default('requires', [])
        self.set_default('is_linear', False)
        self.set_default('dtype', nm.float64)
        self.set_default('term_mode', None)
        self.set_default('set_volume', 'total')

        # Application-specific options.
        self.app_options = self.process_options()

    def process_options(self):
        """
        Setup application-specific options.

        Subclasses should implement this method as needed.

        Returns
        -------
        app_options : Struct instance
            The application options.
        """

    def init_solvers(self, problem):
        """
        Setup solvers. Use local options if these are defined,
        otherwise use the global ones.

        For linear problems, assemble the matrix and try to presolve the
        linear system.
        """

        if hasattr(self, 'solvers'):
            opts = self.solvers

        else:
            opts = problem.conf.options

        problem.set_conf_solvers(problem.conf.solvers, opts)
        problem.init_solvers()

        if self.is_linear:
            output('linear problem, trying to presolve...')
            timer = Timer(start=True)

            ev = problem.get_evaluator()

            state = problem.create_state()
            try:
                mtx_a = ev.eval_tangent_matrix(state(), is_full=True)
            except ValueError:
                output('matrix evaluation failed, giving up...')
                raise

            problem.set_linear(True)
            problem.try_presolve(mtx_a)

            output('...done in %.2f s' % timer.stop())

        else:
            problem.set_linear(False)

    def _get_volume(self, volume):
        if isinstance(volume, dict):
            return volume[self.set_volume]

        else:
            return volume

class CorrSolution(Struct):
    """
    Class for holding solutions of corrector problems.
    """

    def iter_solutions(self):
        if hasattr(self, 'components'):
            for indx in self.components:
                key = ('%d' * len(indx)) % indx
                yield key, self.states[indx]

        else:
            yield '', self.state

    def iter_time_steps(self):
        if hasattr(self, 'n_step') and self.n_step > 0:
            for ii in range(self.n_step):
                yield self.get_ts_val(ii)
        else:
            yield self

    def get_ts_val(self, step):
        if hasattr(self, 'states'):
            states = nm.zeros(self.states.shape, dtype=object)
            for idx in self.components:
                state = {k: v[step] for k, v in\
                         six.iteritems(self.states[idx])}
                states[idx] = state

            out = CorrSolution(name=self.name,
                               states=states,
                               components=self.components)

        else:
            state = {k: v[step] for k, v in six.iteritems(self.state)}
            out = CorrSolution(name=self.name,
                               state=state)

        return out

    def get_output(self, is_dump=False, var_map=None):

        out = {}
        for key, sol in self.iter_solutions():
            for var_name in sol.keys():
                if var_map is not None and var_name in var_map:
                    vname = var_map[var_name]
                else:
                    vname = var_name

                dof_vector = sol[var_name]
                if len(dof_vector.shape) == 1:
                    dof_vector = dof_vector[:, None]

                if is_dump:
                    skey = var_name + '_' + key if key else var_name
                    out[skey] = Struct(name='dump', mode='vertex',
                                       data=dof_vector,
                                       shape=dof_vector.shape,
                                       var_name=vname)
                else:
                    new_key = var_name + '_' + key if key else var_name
                    out[new_key] = dof_vector

        return out


class CorrMiniApp(MiniAppBase):

    def __init__(self, name, problem, kwargs):
        MiniAppBase.__init__(self, name, problem, kwargs)
        self.output_dir = self.problem.output_dir
        self.set_default('save_name', None)

        if self.save_name is not None:
            self.save_name = os.path.normpath(os.path.join(self.output_dir,
                                                           self.save_name))

    def setup_output(self, save_formats=None, post_process_hook=None,
                     split_results_by=None):
        """Instance attributes have precedence!"""
        self.set_default('save_formats', save_formats)
        self.set_default('post_process_hook', post_process_hook)
        self.set_default('split_results_by', split_results_by)

    def get_save_name_base(self):
        return self.save_name

    def get_save_name(self, save_format='.h5', stamp=''):
        save_name_base = self.get_save_name_base()
        if save_name_base is not None:
            return '.'.join((save_name_base + stamp, save_format))

    def get_output(self, corr_sol, is_dump=False, extend=True,
                   variables=None, var_map=None):
        if variables is None:
            variables = self.problem.get_variables()
        to_output = variables.create_output

        if is_dump:
            extend = False

        out = {}
        for key, sol in corr_sol.iter_solutions():
            for var_name in six.iterkeys(sol):
                if var_name not in variables.ordered_state\
                    and var_map is not None\
                    and var_name in var_map:
                    vname = var_map[var_name]
                else:
                    vname = var_name

                dof_vector = sol[var_name]

                if is_dump:
                    skey = var_name + '_' + key if key else var_name
                    var = variables[vname]
                    shape = (var.n_dof // var.n_components,
                             var.n_components)
                    out[skey] = Struct(name='dump', mode='vertex',
                                       data=dof_vector,
                                       shape=shape,
                                       var_name=vname,
                                       region_name=var.field.region.name)

                else:
                    aux = to_output(dof_vector,
                                    var_info={vname: (True, var_name)},
                                    extend=extend)
                    if self.post_process_hook is not None:
                        aux = self.post_process_hook(aux, self.problem,
                                                     None,
                                                     extend=extend)

                    for _key, val in six.iteritems(aux):
                        if key:
                            new_key = _key + '_' + key

                        else:
                            new_key = _key
                        out[new_key] = val

        return out

    def save(self, state, problem, variables=None, ts=None, var_map=None):
        if ts is not None:
            n_digit = int(nm.log10(ts.n_step)) + 1
            time_stamp = ('_%s' % ('%%0%dd' % n_digit)) % ts.step
        else:
            time_stamp = ''

        for save_format in self.save_formats:
            if self.get_save_name_base() is not None:
                if save_format in ['h5']:
                    save_name = self.get_save_name(save_format)
                    is_dump, split_results_by, extend = True, 'none', False
                else:
                    save_name = self.get_save_name(save_format, time_stamp)
                    split_results_by, is_dump = self.split_results_by, False
                    extend = split_results_by is None

                out = self.get_output(state, extend=extend, is_dump=is_dump,
                                      variables=variables, var_map=var_map)

                problem.save_state(save_name, out=out,
                                   split_results_by=split_results_by, ts=ts)

class ShapeDimDim(CorrMiniApp):

    def __call__(self, problem=None, data=None):
        problem = get_default(problem, self.problem)

        clist, pis = create_pis(problem, self.variables[0])

        corr_sol = CorrSolution(name=self.name,
                                states=pis,
                                components=clist)
        self.save(corr_sol, problem,
                  variables=problem.create_variables([self.variables[0]]))

        return corr_sol

class ShapeDim(CorrMiniApp):

    def __call__(self, problem=None, data=None):
        problem = get_default(problem, self.problem)

        clist, pis = create_scalar_pis(problem, self.variables[0])

        corr_sol = CorrSolution(name=self.name,
                                states=pis,
                                components=clist)

        self.save(corr_sol, problem,
                  variables=problem.create_variables([self.variables[0]]))

        return corr_sol

class OnesDim(CorrMiniApp):

    def __call__(self, problem=None, data=None):
        problem = get_default(problem, self.problem)
        var_name = self.variables[0]
        var = problem.get_variables(auto_create=True)[var_name]

        dim = problem.domain.mesh.dim
        nnod = var.n_nod
        e00 = nm.zeros((nnod, dim), dtype=var.dtype)
        e1 = nm.ones((nnod,), dtype=var.dtype)

        ones = nm.zeros((dim,), dtype=object)
        clist = []
        for ir in range(dim):
            aux = e00.copy()
            aux[:,ir] = e1
            ones[ir] = {var_name : nm.ascontiguousarray(aux)}
            clist.append((ir,))

        corr_sol = CorrSolution(name=self.name,
                                states=ones,
                                components=clist)

        self.save(corr_sol, problem,
                  variables=problem.create_variables([self.variables[0]]))

        return corr_sol


class CorrEval(CorrMiniApp):
    def __call__(self, problem=None, data=None):
        problem = get_default(problem, self.problem)
        expr = self.expression
        for req in map(rm_multi, self.requires):
            expr = expr.replace(req, "data['%s']" % req)

        val = eval(expr)


        if type(val) is dict:
            corr_sol = CorrSolution(name=self.name,
                                    state=val)
        elif type(val) is nm.ndarray:
            if val.dtype == object:
                corr_sol = CorrSolution(name=self.name,
                                        states=val,
                                        components=['data'])
            else:
                ndof, ndim = val.shape
                state = {self.variable: val.reshape((ndof * ndim,))}
                corr_sol = CorrSolution(name=self.name,
                                        state=state)
        else:
            corr_sol = val

        cvars = problem.create_variables([self.variable])
        self.save(corr_sol, problem, variables=cvars)

        return corr_sol


class CorrNN(CorrMiniApp):
    """ __init__() kwargs:
        {
             'ebcs' : [],
             'epbcs' : [],
             'equations' : {},
             'set_variables' : None,
        },
    """

    def set_variables_default(variables, ir, ic, set_var, data):
        for (var, req, comp) in set_var:
            variables[var].set_data(data[req].states[ir,ic][comp])

    set_variables_default = staticmethod(set_variables_default)

    def __init__(self, name, problem, kwargs):
        """When dim is not in kwargs, problem dimension is used."""
        CorrMiniApp.__init__(self, name, problem, kwargs)
        self.set_default('dim', problem.get_dim())

    def __call__(self, problem=None, data=None):
        problem = get_default(problem, self.problem)

        problem.set_equations(self.equations)

        problem.select_bcs(ebc_names=self.ebcs, epbc_names=self.epbcs,
                           lcbc_names=self.get('lcbcs', []))

        problem.update_materials(problem.ts)

        self.init_solvers(problem)

        variables = problem.get_variables()

        states = nm.zeros((self.dim, self.dim), dtype=object)
        clist = []
        for ir in range(self.dim):
            for ic in range(self.dim):
                if isinstance(self.set_variables, list):
                    self.set_variables_default(variables, ir, ic,
                                               self.set_variables, data)
                else:
                    self.set_variables(variables, ir, ic, **data)

                state = problem.solve(update_materials=False,
                                      save_results=False)
                assert_(state.has_ebc())
                states[ir,ic] = state.get_state_parts()

                clist.append((ir, ic))

        corr_sol = CorrSolution(name=self.name,
                                states=states,
                                components=clist)

        self.save(corr_sol, problem)

        return corr_sol

class CorrN(CorrMiniApp):

    def set_variables_default(variables, ir, set_var, data):
        for (var, req, comp) in set_var:
            variables[var].set_data(data[req].states[ir][comp])

    set_variables_default = staticmethod(set_variables_default)

    def __init__(self, name, problem, kwargs):
        """When dim is not in kwargs, problem dimension is used."""
        CorrMiniApp.__init__(self, name, problem, kwargs)
        self.set_default('dim', problem.get_dim())

    def __call__(self, problem=None, data=None):
        problem = get_default(problem, self.problem)

        problem.set_equations(self.equations)

        problem.select_bcs(ebc_names=self.ebcs, epbc_names=self.epbcs,
                           lcbc_names=self.get('lcbcs', []))

        problem.update_materials(problem.ts)

        self.init_solvers(problem)

        variables = problem.get_variables()

        states = nm.zeros((self.dim,), dtype=object)
        clist = []
        for ir in range(self.dim):
            if isinstance(self.set_variables, list):
                self.set_variables_default(variables, ir,
                                           self.set_variables, data)
            else:
                self.set_variables(variables, ir, **data)
            state = problem.solve(update_materials=False,
                                  save_results=False)
            assert_(state.has_ebc())
            states[ir] = state.get_state_parts()

            clist.append((ir,))

        corr_sol = CorrSolution(name=self.name,
                                states=states,
                                components=clist)

        self.save(corr_sol, problem)

        return corr_sol

class CorrDimDim(CorrNN):
    pass

class CorrDim(CorrN):
    pass

class CorrOne(CorrMiniApp):

    def set_variables_default(variables, set_var, data):
        for (var, req, comp) in set_var:
            variables[var].set_data(data[req].state[comp])

    set_variables_default = staticmethod(set_variables_default)

    def __call__(self, problem=None, data=None):
        problem = get_default(problem, self.problem)

        problem.set_equations(self.equations)

        problem.select_bcs(ebc_names=self.ebcs, epbc_names=self.epbcs,
                           lcbc_names=self.get('lcbcs', []))

        problem.update_materials(problem.ts)

        self.init_solvers(problem)

        variables = problem.get_variables()

        if hasattr(self, 'set_variables'):
            if isinstance(self.set_variables, list):
                self.set_variables_default(variables, self.set_variables,
                                           data)
            else:
                self.set_variables(variables, **data)

        state = problem.solve(update_materials=False,
                              save_results=False)
        assert_(state.has_ebc())

        corr_sol = CorrSolution(name=self.name,
                                state=state.get_state_parts())

        self.save(corr_sol, problem)

        return corr_sol

class CorrSetBCS(CorrMiniApp):

    def __call__(self, problem=None, data=None):
        from sfepy.base.base import select_by_names
        from sfepy.discrete.variables import Variables
        from sfepy.discrete.conditions import Conditions

        problem = get_default(problem, self.problem)

        conf_ebc = select_by_names(problem.conf.ebcs, self.ebcs)
        conf_epbc = select_by_names(problem.conf.epbcs, self.epbcs)
        ebcs = Conditions.from_conf(conf_ebc, problem.domain.regions)
        epbcs = Conditions.from_conf(conf_epbc, problem.domain.regions)

        conf_variables = select_by_names(problem.conf.variables, self.variable)
        variables = Variables.from_conf(conf_variables, problem.fields)
        variables.equation_mapping(ebcs, epbcs, problem.ts, problem.functions)
        variables.init_state()
        variables.fill_state(0.0)
        variables.apply_ebc()

        corr_sol = CorrSolution(name=self.name,
                                state=variables.get_state_parts())

        self.save(corr_sol, problem, variables=variables)

        return corr_sol

class CorrEqPar(CorrOne):
    """
    The corrector which equation can be parametrized via 'eq_pars',
    the dimension is given by the number of parameters.

    Example:

        'equations': 'dw_diffusion.5.Y(mat.k, q, p) =
                      dw_integrate.5.%s(q)',
        'eq_pars': ('bYMp', 'bYMm'),
        'class': cb.CorrEqPar,

    """

    def __init__(self, name, problem, kwargs):
        """When dim is not in kwargs, problem dimension is used."""
        CorrMiniApp.__init__(self, name, problem, kwargs)
        self.set_default('dim', len(self.eq_pars))

    def __call__(self, problem=None, data=None):
        problem = get_default(problem, self.problem)

        states = nm.zeros((self.dim,), dtype=object)
        clist = []

        eqns ={}
        for ir in range(self.dim):
            for key_eq, val_eq in six.iteritems(self.equations):
                eqns[key_eq] = val_eq % self.eq_pars[ir]

            problem.set_equations(eqns)

            problem.select_bcs(ebc_names=self.ebcs, epbc_names=self.epbcs,
                               lcbc_names=self.get('lcbcs', []))

            problem.update_materials(problem.ts)

            self.init_solvers(problem)

            variables = problem.get_variables()

            if hasattr(self, 'set_variables'):
                if isinstance(self.set_variables, list):
                    self.set_variables_default(variables, self.set_variables,
                                               data)
                else:
                    self.set_variables(variables, **data)

            state = problem.solve(update_materials=False,
                                  save_results=False)
            assert_(state.has_ebc())

            states[ir] = state.get_state_parts()
            clist.append((ir,))

        corr_sol = CorrSolution(name=self.name,
                                states=states,
                                components=clist)

        self.save(corr_sol, problem)

        return corr_sol

class PressureEigenvalueProblem(CorrMiniApp):
    """Pressure eigenvalue problem solver for time-dependent correctors."""

    def presolve(self, mtx):
        """Prepare A^{-1} B^T for the Schur complement."""

        mtx_a = mtx['A']
        mtx_bt = mtx['BT']
        output('full A size: %.3f MB' % (8.0 * nm.prod(mtx_a.shape) / 1e6))
        output('full B size: %.3f MB' % (8.0 * nm.prod(mtx_bt.shape) / 1e6))

        ls = Solver.any_from_conf(self.problem.ls_conf
                                  + Struct(use_presolve=True), mtx=mtx_a)
        if self.mode == 'explicit':
            timer = Timer(start=True)
            mtx_aibt = nm.zeros(mtx_bt.shape, dtype=mtx_bt.dtype)
            for ic in range(mtx_bt.shape[1]):
                mtx_aibt[:,ic] = ls(mtx_bt[:,ic].toarray().squeeze())
            output('mtx_aibt: %.2f s' % timer.stop())
            action_aibt = MatrixAction.from_array(mtx_aibt)
        else:
            ##
            # c: 30.08.2007, r: 13.02.2008
            def fun_aibt(vec):
                # Fix me for sparse mtx_bt...
                rhs = sc.dot(mtx_bt, vec)
                out = ls(rhs)
                return out
            action_aibt = MatrixAction.from_function(fun_aibt,
                                                    (mtx_a.shape[0],
                                                     mtx_bt.shape[1]),
                                                    nm.float64)
        mtx['action_aibt'] = action_aibt

    def solve_pressure_eigenproblem(self, mtx, eig_problem=None,
                                    n_eigs=0, check=False):
        """G = B*AI*BT or B*AI*BT+D"""

        def get_slice(n_eigs, nn):
            if n_eigs > 0:
                ii = slice(0, n_eigs)
            elif n_eigs < 0:
                ii = slice(nn + n_eigs, nn)
            else:
                ii = slice(0, 0)
            return ii

        eig_problem = get_default(eig_problem, self.eig_problem)
        n_eigs = get_default(n_eigs, self.n_eigs)
        check = get_default(check, self.check)

        mtx_c, mtx_b, action_aibt = mtx['C'], mtx['B'], mtx['action_aibt']
        mtx_g = mtx_b * action_aibt.to_array() # mtx_b must be sparse!
        if eig_problem == 'B*AI*BT+D':
            mtx_g += mtx['D'].toarray()

        mtx['G'] = mtx_g
        output(mtx_c.shape, mtx_g.shape)

        eigs, mtx_q = eig(mtx_c.toarray(), mtx_g, solver_kind='eig.sgscipy')

        if check:
            ee = nm.diag(sc.dot(mtx_q.T * mtx_c, mtx_q)).squeeze()
            oo = nm.diag(sc.dot(sc.dot(mtx_q.T,  mtx_g), mtx_q)).squeeze()
            try:
                assert_(nm.allclose(ee, eigs))
                assert_(nm.allclose(oo, nm.ones_like(eigs)))
            except ValueError:
                debug()

        nn = mtx_c.shape[0]
        if isinstance(n_eigs, tuple):
            output('required number of eigenvalues: (%d, %d)' % n_eigs)
            if sum(n_eigs) < nn:
                ii0 = get_slice(n_eigs[0], nn)
                ii1 = get_slice(-n_eigs[1], nn)
                eigs = nm.concatenate((eigs[ii0], eigs[ii1]))
                mtx_q = nm.concatenate((mtx_q[:,ii0], mtx_q[:,ii1]), 1)
        else:
            output('required number of eigenvalues: %d' % n_eigs)
            if (n_eigs != 0) and (abs(n_eigs) < nn):
                ii = get_slice(n_eigs, nn)
                eigs = eigs[ii]
                mtx_q = mtx_q[:,ii]

        out = Struct(eigs=eigs, mtx_q=mtx_q)
        return out

    def __call__(self, problem=None, data=None):
        problem = get_default(problem, self.problem)

        problem.set_equations(self.equations)
        problem.select_bcs(ebc_names=self.ebcs, epbc_names=self.epbcs,
                           lcbc_names=self.get('lcbcs', []))
        problem.update_materials()

        mtx = problem.equations.eval_tangent_matrices(problem.create_state()(),
                                                      problem.mtx_a,
                                                      by_blocks=True)
        self.presolve(mtx)

        evp = self.solve_pressure_eigenproblem(mtx)
        return Struct(name=self.name, ebcs=self.ebcs, epbcs=self.epbcs,
                      mtx=mtx, evp=evp)

class TCorrectorsViaPressureEVP(CorrMiniApp):
    """
    Time correctors via the pressure eigenvalue problem.
    """

    def setup_equations(self, equations, problem=None):
        """
        Set equations, update boundary conditions and materials.
        """
        problem = get_default(problem, self.problem)

        problem.set_variables()
        problem.set_equations(equations)
        problem.select_bcs(ebc_names=self.ebcs, epbc_names=self.epbcs,
                           lcbc_names=self.get('lcbcs', []))
        problem.update_materials() # Assume parameters constant in time.

    def compute_correctors(self, evp, sign, state0, ts,
                           problem=None, vec_g=None):
        problem = get_default(problem, self.problem)

        eigs = evp.evp.eigs
        mtx_q = evp.evp.mtx_q
        mtx = evp.mtx

        nr, nc = mtx_q.shape

        if vec_g is not None:
            output('nonzero pressure EBC: max = %e, min = %e' \
                    % (vec_g.max(), vec_g.min()))
            one = nm.ones((nc,), dtype=nm.float64)

        vu, vp = self.up_variables

        variables = problem.get_variables()
        var_u = variables[vu]
        var_p = variables[vp]

        ##
        # follow_epbc = False -> R1 = - R2 as required. ? for other correctors?
        vec_p0 = sign * var_p.get_reduced(state0[vp], follow_epbc=False)

        # xi0 = Q^{-1} p(0) = Q^T G p(0)
        vec_xi0 = sc.dot(mtx_q.T, sc.dot(mtx['G'],
                                           vec_p0[:,nm.newaxis])).squeeze()
        action_aibt = mtx['action_aibt']

        e_e_qg = 0.0
        iee_e_qg = 0.0
        format = '====== time %%e (step %%%dd of %%%dd) ====='\
                 % ((ts.n_digit,) * 2)
        vu, vp = self.up_variables
        state = {k: [] for k in [vu, vp, 'd' + vp]}
        for step, time in ts:
            output(format % (time, step + 1, ts.n_step))

            e_e = nm.exp(- eigs * time)
            e_e_qp = e_e * vec_xi0 # exp(-Et) Q^{-1} p(0)

            if vec_g is not None:
                Qg = sc.dot(mtx_q.T, vec_g)
                e_e_qg = e_e * Qg
                iee_e_qg = ((one - e_e) / eigs) * Qg

            vec_p = sc.dot(mtx_q, e_e_qp + iee_e_qg)
            vec_dp = - sc.dot(mtx_q, (eigs * e_e_qp - e_e_qg))
            vec_u = action_aibt(vec_dp)

            vec_u = var_u.get_full(vec_u)
            vec_p = var_p.get_full(vec_p)
            # BC nodes - time derivative of constant is zero!
            vec_dp = var_p.get_full(vec_dp, force_value=0.0)

            state[vu].append(vec_u)
            state[vp].append(vec_p)
            state['d' + vp].append(vec_dp)

        return {k: nm.asarray(v) for k, v in state.items()}

    def save(self, corrs, problem, ts):
        ts0 = TimeStepper(0, 1)
        ts0.set_from_ts(ts, step=0)
        _, vp = self.up_variables

        for step, _ in ts0:
            icorrs = corrs.get_ts_val(step)
            super(TCorrectorsViaPressureEVP, self).save(icorrs, problem, ts=ts0,
                                                        var_map={'d' + vp: vp})


def create_ts_coef(cls):
    """
    Define a new class with modified call method which accepts
    time dependent data (correctors).
    """
    class TSCoef(cls):

        def __call__(self, volume=None, problem=None, data=None):
            problem = get_default(problem, self.problem)
            ts_keys = []
            ts_data = {}
            n_step = None
            for key, val in six.iteritems(data):
                if isinstance(val, CorrSolution) and hasattr(val, 'n_step'):
                    if n_step is None:
                        n_step = val.n_step
                    else:
                        if not(n_step == val.n_step):
                            raise ValueError('incorrect number of time' +\
                                             'steps in %s!' % self.name)

                    ts_keys.append(key)
                else:
                    ts_data[key] = val

            if n_step is None:
                raise ValueError('no time steps found in %s!' % self.name)

            n_digit = int(nm.log10(n_step))+1
            format = '====== step %%%dd of %%%dd =====' % ((n_digit,) * 2)
            out = []
            for step in range(n_step):
                output(format % (step + 1, n_step))
                for key in ts_keys:
                    ts_data[key] = data[key].get_ts_val(step)
                out.append(cls.__call__(self, volume, problem, ts_data))

            out = nm.asarray(out)
            sh = out.shape
            if len(sh) == 2:
                out = out.reshape((sh[0], 1, sh[1]))
            elif len(sh) == 1:
                out = out.reshape((sh[0], 1, 1))

            return out

    return TSCoef


class CoefDummy(MiniAppBase):
    """
    Dummy class serving for computing and returning its requirements.
    """

    def __call__(self, volume=None, problem=None, data=None):
        return data

class TSTimes(MiniAppBase):
    """Coefficient-like class, returns times of the time stepper."""
    def __call__(self, volume=None, problem=None, data=None):
        problem = get_default(problem, self.problem)
        problem.init_solvers()
        return problem.get_timestepper().times

class VolumeFractions(MiniAppBase):
    """Coefficient-like class, returns volume fractions of given regions within
    the whole domain."""
    def __call__(self, volume=None, problem=None, data=None):
        problem = get_default(problem, self.problem)

        vf = {}
        for region_name in self.regions:
            vkey = 'volume_%s' % region_name
            key = 'fraction_%s' % region_name

            equations, variables = problem.create_evaluable(
                self.expression % region_name)
            val = eval_equations(equations, variables).real

            vf[vkey] = nm.asarray(val, dtype=nm.float64)
            vf[key] = vf[vkey] / self._get_volume(volume)

        return vf


class CoefMN(MiniAppBase):
    @staticmethod
    def set_variables_default(variables, ir, ic, mode, set_var, data, dtype):
        def get_corr_state(corr, ir, ic):
            if hasattr(corr, 'states'):
                if ir is None:
                    return corr.states[ic]
                elif ic is None:
                    return corr.states[ir]
                else:
                    return corr.states[ir, ic]
            else:
                return corr.state

        if mode == 'row_only':
            act_set_var = set_var
        else:
            mode2var = {'row': 0, 'col': 1}
            aux = set_var[mode2var[mode]]
            act_set_var = aux[:] if isinstance(aux, list) else [aux]
            act_set_var += set_var[2:]

        for (var, req, comp) in act_set_var:
            if type(req) is tuple:
                val = get_corr_state(data[req[0]], ir, ic)[comp].copy()
                val = nm.asarray(val, dtype=dtype)
                for ii in req[1:]:
                    val += get_corr_state(data[ii], ir, ic)[comp]

            else:
                val = get_corr_state(data[req], ir, ic)[comp]

            variables[var].set_data(val)

    def __init__(self, name, problem, kwargs):
        """When dim is not in kwargs, problem dimension is used."""
        MiniAppBase.__init__(self, name, problem, kwargs)
        self.set_default('dim', problem.get_dim())

    def get_coef(self, row, col, volume, problem, data):
        problem = get_default(problem, self.problem)
        term_mode = self.term_mode
        equations, variables = problem.create_evaluable(self.expression,
                                                        term_mode=term_mode)

        coef = nm.zeros((len(row), len(col)), dtype=self.dtype)

        for ir, (irr, icr) in enumerate(row):
            if isinstance(self.set_variables, list):
                self.set_variables_default(variables, irr, icr, 'row',
                                           self.set_variables, data,
                                           self.dtype)
            else:
                self.set_variables(variables, irr, icr, 'row', **data)

            for ic, (irc, icc) in enumerate(col):
                if isinstance(self.set_variables, list):
                    self.set_variables_default(variables, irc, icc, 'col',
                                               self.set_variables, data,
                                               self.dtype)
                else:
                    self.set_variables(variables, irc, icc, 'col', **data)

                val = eval_equations(equations, variables, term_mode=term_mode)
                coef[ir, ic] = val

        coef /= self._get_volume(volume)

        return coef

    def __call__(self, volume, problem=None, data=None):
        if isinstance(self.dim, Iterable) and len(self.dim) >= 2:
            dim1, dim2 = self.dim[:2]
        else:
            dim1 = dim2 = self.dim

        row = [(ii, None) for ii in range(dim1)]
        col = [(None, ii) for ii in range(dim2)]

        return self.get_coef(row, col, volume, problem, data)


class CoefDimDim(CoefMN):
    pass


class CoefSymSym(CoefMN):
    iter_sym = staticmethod(iter_sym)
    is_sym = True

    def __call__(self, volume, problem=None, data=None):
        problem = get_default(problem, self.problem)
        isym = [ii for ii in self.iter_sym(problem.get_dim())]

        return self.get_coef(isym, isym, volume, problem, data)


class CoefNonSymNonSym(CoefSymSym):
    iter_sym = staticmethod(iter_nonsym)
    is_sym = False


class CoefDimSym(CoefMN):
    def __call__(self, volume, problem=None, data=None):
        problem = get_default(problem, self.problem)
        dim = problem.get_dim()
        row = [(ii, None) for ii in range(dim)]
        col = [ii for ii in iter_sym(dim)]

        return self.get_coef(row, col, volume, problem, data)


class CoefN(CoefMN):
    @staticmethod
    def set_variables_default(variables, ir, ic, mode, set_var, data, dtype):
        mode = mode + '_only'
        CoefMN.set_variables_default(variables, ir, ic, mode, set_var, data,
                                     dtype)

    def get_coef(self, row, volume, problem, data):
        problem = get_default(problem, self.problem)
        term_mode = self.term_mode
        equations, variables = problem.create_evaluable(self.expression,
                                                        term_mode=term_mode)

        coef = nm.zeros((len(row),), dtype=self.dtype)

        for ii, (ir, ic) in enumerate(row):
            if isinstance(self.set_variables, list):
                self.set_variables_default(variables, ir, ic, 'row',
                                           self.set_variables, data, self.dtype)
            else:
                self.set_variables(variables, ir, ic, 'row', **data)

            val = eval_equations(equations, variables, term_mode=term_mode)
            coef[ii] = val

        coef /= self._get_volume(volume)

        return coef

    def __call__(self, volume, problem=None, data=None):
        row = [(ii, None) for ii in range(self.dim)]

        return self.get_coef(row, volume, problem, data)


class CoefDim(CoefN):
    pass


class CoefSym(CoefN):
    iter_sym = staticmethod(iter_sym)
    is_sym = True

    def __call__(self, volume, problem=None, data=None):
        problem = get_default(problem, self.problem)
        isym = [ii for ii in self.iter_sym(problem.get_dim())]

        return self.get_coef(isym, volume, problem, data)


class CoefNonSym(CoefSym):
    iter_sym = staticmethod(iter_nonsym)
    is_sym = False


class CoefOne(MiniAppBase):

    def set_variables_default(variables, set_var, data, dtype):
        for (var, req, comp) in set_var:
            if type(req) is tuple:
                val = data[req[0]].state[comp].copy()
                val = nm.asarray(val, dtype=dtype)
                for ii in req[1:]:
                    val += data[ii].state[comp]

            else:
                val = data[req].state[comp]

            variables[var].set_data(val)

    set_variables_default = staticmethod(set_variables_default)

    def __call__(self, volume, problem=None, data=None):
        problem = get_default(problem, self.problem)

        term_mode = self.term_mode
        equations, variables = problem.create_evaluable(self.expression,
                                                        term_mode=term_mode)

        if hasattr(self, 'set_variables'):
            if isinstance(self.set_variables, list):
                self.set_variables_default(variables, self.set_variables,
                                           data, self.dtype)
            else:
                self.set_variables(variables, **data)

        val = eval_equations(equations, variables,
                             term_mode=term_mode)

        coef = val / self._get_volume(volume)

        return coef


class CoefSum(MiniAppBase):

    def __call__(self, volume, problem=None, data=None):
        coef = nm.zeros_like(data[self.requires[0]])
        for req in map(rm_multi, self.requires):
            coef += data[req]

        return coef

class CoefEval(MiniAppBase):
    """
    Evaluate expression.
    """
    def __call__(self, volume, problem=None, data=None):
        expr = self.expression
        for req in map(rm_multi, self.requires):
            expr = expr.replace(req, "data['%s']" % req)

        coef = eval(expr)

        return coef

class CoefNone(MiniAppBase):

    def __call__(self, volume, problem=None, data=None):

        coef = 0.0

        return coef

class CoefExprPar(MiniAppBase):
    """
    The coefficient which expression can be parametrized via 'expr_pars',
    the dimension is given by the number of parameters.

    Example:

        'expression': 'dw_surface_ndot.5.Ys(mat_norm.k%d, corr1)',
        'expr_pars': [ii for ii in range(dim)],
        'class': cb.CoefExprPar,

    """
    def set_variables_default(variables, ir, set_var, data):
        for (var, req, comp) in set_var:
            if hasattr(data[req], 'states'):
                variables[var].set_data(data[req].states[ir][comp])

            else:
                variables[var].set_data(data[req].state[comp])

    set_variables_default = staticmethod(set_variables_default)

    def __init__(self, name, problem, kwargs):
        """When dim is not in kwargs, problem dimension is used."""
        MiniAppBase.__init__(self, name, problem, kwargs)
        dim = len(self.expr_pars)
        self.set_default('dim', dim)

    def __call__(self, volume, problem=None, data=None):
        problem = get_default(problem, self.problem)

        coef = nm.zeros((self.dim,), dtype=self.dtype)
        term_mode = self.term_mode

        for ir in range(self.dim):
            expression = self.expression % self.expr_pars[ir]
            equations, variables = \
              problem.create_evaluable(expression, term_mode=term_mode)

            if hasattr(self, 'set_variables'):
                if isinstance(self.set_variables, list):
                    self.set_variables_default(variables, ir,
                                               self.set_variables, data)
                else:
                    self.set_variables(variables, ir, **data)

            val = eval_equations(equations, variables,
                                 term_mode=term_mode)
            coef[ir] = val

        coef /= self._get_volume(volume)

        return coef
