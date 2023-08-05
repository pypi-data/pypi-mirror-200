.. _acoustics-vibro_acoustic3d_mid:

acoustics/vibro_acoustic3d_mid.py
=================================

**Description**


Vibro-acoustic problem

3D acoustic domain with 2D perforated deforming interface.

*Master problem*: defined in 3D acoustic domain (``vibro_acoustic3d.py``)

*Slave subproblem*: 2D perforated interface (``vibro_acoustic3d_mid.py``)

Master 3D problem - find :math:`p` (acoustic pressure)
and :math:`g` (transversal acoustic velocity) such that:

.. math::
    c^2 \int_{\Omega} \nabla q \cdot \nabla p
    - \omega^2 \int_{\Omega} q p
    + i \omega c \int_{\Gamma_{in}} q p
    + i \omega c \int_{\Gamma_{out}} q p
    - i \omega c^2 \int_{\Gamma_0} (q^+ - q^-) g
    = 2i \omega c \int_{\Gamma_{in}} q \bar{p}
    \;, \quad \forall q \;,

    - i \omega \int_{\Gamma_0} f (p^+ - p^-)
    - \omega^2 \int_{\Gamma_0} F f g
    + \omega^2 \int_{\Gamma_0} C f w
    = 0
    \;, \quad \forall f \;,

Slave 2D subproblem - find :math:`w` (plate deflection)
and :math:`\ul{\theta}` (rotation) such that:

.. math::
    \omega^2 \int_{\Gamma_0} C z g
    - \omega^2 \int_{\Gamma_0} S z w
    + \int_{\Gamma_0} \nabla z \cdot \ull{G} \cdot \nabla w
    - \int_{\Gamma_0} \ul{\theta} \cdot \ull{G} \cdot \nabla z
    = 0
    \;, \quad \forall z \;,

    - \omega^2 \int_{\Gamma_0} R\, \ul{\nu} \cdot \ul{\theta}
    + \int_{\Gamma_0} D_{ijkl} e_{ij}(\ul{\nu}) e_{kl}(\ul{\theta})
    - \int_{\Gamma_0} \ul{\nu} \cdot \ull{G} \cdot \nabla w
    + \int_{\Gamma_0} \ul{\nu} \cdot \ull{G} \cdot \ul{\theta}
    = 0
    \;, \quad \forall \ul{\nu} \;,




:download:`source code </../sfepy/examples/acoustics/vibro_acoustic3d_mid.py>`

.. literalinclude:: /../sfepy/examples/acoustics/vibro_acoustic3d_mid.py

