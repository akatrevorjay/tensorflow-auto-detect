tensorflow-auto-detect
=============================

Solves the absolute mess that is installing `tensorflow` from your package requirements.

Just put it in your setuptools requirements and it'll install the GPU version of tensorflow if you have a CUDA
available; otherwise it will fallback to the CPU version.

|ci-badge| |coverage-badge|

- PyPi: https://pypi.python.org/pypi/tensorflow-auto-detect
- Docs: All you need is right on this page.


The problem
-----------

Background: Tensorflow provides two pypi packages: `tensorflow` and `tensorflow-gpu`.
I'm sure you can infer which is compiled for which.

Let's say you're making a product or have a project:

- It uses Tensorflow.

- It will run on a myriad of classes of machines, and therefore needs to be able to operate and install on machines that may or may not have CUDA available.

- You want your package to be easily installable. Every time. Not just for half of your userbase.

- You don't want to have toss the problem on your users and fellow engineers.

Let's be honest, your stringently detailed absoute step-by-step microbe resistant instructions could.. *maybe..*
*possibly..* not be followed and/or remembered exactly to a tee. You know, like everything else.

**Q:** How do you add the proper one to your own package as a requirement when they both install to the same package namespace?

**A:** Well, **you can't**, son. 🕶  *Oh, and by the way, if you install one after the other, say to fix if you installed
the wrong one at first (it's okay it's unintuitive), I'll just blindly trample over the first's files instead of doing
anything useful. (yada yada setuptools yada)*

You can try to choke it down with sweet hacks like:

- Adding each in their own `extras_require` blocks
  (ruining your default and therefore path of least resistance)

- Toss the problem onto the user. You're *that guy* now.


How does it work?
-----------------

This package includes a list of all libraries required by each version of tensorflow in `tfdetect/cuda.py`.

Currently, only the check for the cuda runtime library is active (by design) to be a bit more forgiving and allowing for
"strange" setups, even though I've yet to come across one. This is the finest heuristic for this anyway, so it works out
nicely, even in the face of your sweet sweet custom compiles; not to mention ensuring optional dependencies stay that way.

*For versions below `1.7`* `pkg-config` was interrogated, which while that works, it required development headers.
The current method outlined above does not require headers to be available, and works in all sane configurations of
your systems including minimal containers, as long as you have the cuda runtime on your system.


Usage
-----

In `requirements.txt` or `install_requires`:

.. code:: sh

    tensorflow-auto-detect==1.10.0  # or any other release, 1to1 mapping to tf releases

As `pip` argument:

.. code:: sh

    pip install tensorflow-auto-detect==1.8.1  # or any other release, 1to1 mapping to tf releases


Running tests
-------------

.. code:: sh

    pip install '.[tests]'
    pytest


.. |ci-badge| image:: https://circleci.com/gh/akatrevorjay/tensorflow-auto-detect.svg?style=svg
   :target: https://circleci.com/gh/akatrevorjay/tensorflow-auto-detect
.. |coverage-badge| image:: https://coveralls.io/repos/akatrevorjay/tensorflow-auto-detect/badge.svg?branch=develop&service=github
   :target: https://coveralls.io/github/akatrevorjay/tensorflow-auto-detect?branch=develop

