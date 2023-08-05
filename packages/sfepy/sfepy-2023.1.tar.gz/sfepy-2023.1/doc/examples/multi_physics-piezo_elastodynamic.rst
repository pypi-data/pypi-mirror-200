.. _multi_physics-piezo_elastodynamic:

multi_physics/piezo_elastodynamic.py
====================================

**Description**


The linear elastodynamics of a piezoelectric body loaded by a given base
motion.

Find the displacements :math:`\ul{u}(t)` and potential :math:`p(t)` such that:

.. math::
    - \int_\Omega \rho\ \ul{v} \cdot \ul{\ddot u}
    + \int_\Omega C_{ijkl}\ \veps_{ij}(\ul{v}) \veps_{kl}(\ul{u})
    - \int_\Omega e_{kij}\ \veps_{ij}(\ul{v}) \nabla_k p
    = 0
    \;, \quad \forall \ul{v} \;,

    \int_\Omega e_{kij}\ \veps_{ij}(\ul{u}) \nabla_k q
    + \int_\Omega \kappa_{ij} \nabla_i \psi \nabla_j p
    = 0
    \;, \quad \forall q \;,

where :math:`C_{ijkl}` is the matrix of elastic properties under constant
electric field intensity, :math:`e_{kij}` the piezoelectric modulus and
:math:`\kappa_{ij}` the permittivity under constant deformation.

Usage Examples
--------------

Run with the default settings, results stored in ``output/piezo-ed/``::

  sfepy-run sfepy/examples/multi_physics/piezo_elastodynamic.py

The :func:`define()` arguments, see below, can be set using the ``-d`` option::

  sfepy-run sfepy/examples/multi_physics/piezo_elastodynamic.py -d "order=2, ct1=2.5"

View the resulting potential :math:`p` on a deformed mesh (2000x magnified)::

  sfepy-view output/piezo-ed/user_block.h5 -f p:wu:f2000:p0 1:vw:wu:f2000:p0 --color-map=seismic


.. image:: /../doc/images/gallery/multi_physics-piezo_elastodynamic.png


:download:`source code </../sfepy/examples/multi_physics/piezo_elastodynamic.py>`

.. literalinclude:: /../sfepy/examples/multi_physics/piezo_elastodynamic.py

