# tensorflow-detect

Solves the absolute mess that is installing `tensorflow` from your package requirements.

Just put it in your setuptools requirements and it'll install the GPU version of tensorflow if you have a CUDA
available; otherwise it will fallback to the CPU version.

Requires `pkg-config` to be on your system, which is nearly a given.

