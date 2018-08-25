# tensorflow-auto-detect-cpugpu

Solves the absolute mess that is installing `tensorflow` from your package requirements.

Just put it in your setuptools requirements and it'll install the GPU version of tensorflow if you have a CUDA
available; otherwise it will fallback to the CPU version.

## The problem

Say you're making a product.

It uses Tensorflow.

It will run on a myriad of classes of machines, and needs to be able to
operate and install on machines with CUDA available and machines that do not.

Tensorflow provides two pypi packages: `tensorflow` and `tensorflow-gpu`. I'm sure you can infer which is compiled for which.

To make matters worse: *Installing one blindly tramples over the other.* (because yada yada setuptools yada)

**Q:** How do you add the proper one to your own package as a requirement when they both install to the same package namespace?

**A:** *Well, you can't.* You can only try desperately to work around it with hacks like adding each in their own
`extras_require` block or toss the problem onto the user like a pleb. *... but these are not solutions, are they?*


## How does it work?

This package includes a list of all libraries required by each version of tensorflow in `tfdetect/cuda.py`.

Currently, only the check for the cuda runtime library is active (by design) to be a bit more forgiving and allowing for
"strange" setups, even though I've yet to come across one. This is the finest heuristic for this anyway, so it works out
nicely, even in the face of your sweet sweet custom compiles; not to mention ensuring optional dependencies stay that way.

*For versions below `1.7`* `pkg-config` was interrogated, which while that works, it required development headers.
The current method outlined above does not require headers to be available, and works in all sane configurations of
your systems including minimal containers, as long as you have the cuda runtime on your system.


## Example

In `requirements.txt` or `install_requires`:

```
tensorflow-auto-detect-cpugpu==1.10.0  # or any other release, 1to1 mapping to tf releases
```

As pip argument:

```sh
pip install tensorflow-auto-detect-cpucpu==1.8.1  # or any other release, 1to1 mapping to tf releases
```

