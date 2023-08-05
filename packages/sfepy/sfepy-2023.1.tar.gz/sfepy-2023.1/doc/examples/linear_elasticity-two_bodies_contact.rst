.. _linear_elasticity-two_bodies_contact:

linear_elasticity/two_bodies_contact.py
=======================================

**Description**


Contact of two elastic bodies with a penalty function for enforcing the contact
constraints.

Find :math:`\ul{u}` such that:

.. math::
    \int_{\Omega} D_{ijkl}\ e_{ij}(\ul{v}) e_{kl}(\ul{u})
    + \int_{\Gamma_{c}} \varepsilon_N \langle g_N(\ul{u}) \rangle \ul{n} \ul{v}
    = 0
    \;, \quad \forall \ul{v} \;,

where :math:`\varepsilon_N \langle g_N(\ul{u}) \rangle` is the penalty
function, :math:`\varepsilon_N` is the normal penalty parameter, :math:`\langle
g_N(\ul{u}) \rangle` are the Macaulay's brackets of the gap function
:math:`g_N(\ul{u})` and

.. math::
    D_{ijkl} = \mu (\delta_{ik} \delta_{jl}+\delta_{il} \delta_{jk}) +
    \lambda \ \delta_{ij} \delta_{kl}
    \;.

Usage examples::

  sfepy-run sfepy/examples/linear_elasticity/two_bodies_contact.py --save-regions-as-groups --save-ebc-nodes

  sfepy-view two_bodies.mesh.vtk -f u:wu:f2:p0 1:vw:p0 gap:p1 -2

  python3 sfepy/scripts/plot_logs.py log.txt

  sfepy-view two_bodies.mesh_ebc_nodes.vtk -2
  sfepy-view two_bodies.mesh_regions.vtk -2


.. image:: /../doc/images/gallery/linear_elasticity-two_bodies_contact.png


:download:`source code </../sfepy/examples/linear_elasticity/two_bodies_contact.py>`

.. literalinclude:: /../sfepy/examples/linear_elasticity/two_bodies_contact.py

