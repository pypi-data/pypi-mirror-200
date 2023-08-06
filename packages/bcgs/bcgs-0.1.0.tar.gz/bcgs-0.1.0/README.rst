.. image:: https://img.shields.io/pypi/v/bcgs.svg
   :alt: PyPi
   :target: https://pypi.python.org/pypi/bcgs
.. image:: https://img.shields.io/pypi/l/bcgs.svg
   :alt: BSD-3
   :target: https://opensource.org/licenses/BSD-3-Clause

=====================================================================================
Bayesian Conjugate Gibbs Sampler (BCGS)
=====================================================================================

-------------------------------------------
Lightweight, pure-Python conjugate sampling
-------------------------------------------

BCGS is an implementation of Markov chain monte carlo using conjugate Gibbs sampling for performing Bayesian inference. Compared to software like JAGS and BUGS, BCGS is extremely crude and limited. It exists mainly for pedagogical purposes. It may also be a convenient solution for simple inference problems, as it is written in pure Python, with no dependences beyond ``numpy`` and ``scipy``, and requires no special installation.

Installation
============

Either ``pip install bcgs`` or just download the source ``bcgs/bcgs.py`` file from the repository.


Documentation
=============

See the associated `github.io page <https://abmantz.github.io/bcgs/>`_. The notebook from which it is generated can be found `here <https://github.com/abmantz/bcgs/tree/main/examples>`_.
