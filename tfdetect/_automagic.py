#!/usr/bin/env python

import logging
import pkg_resources

log = logging.getLogger(__name__)

# __version__ = pkg_resources.get_distribution(__name__).version
# __version__ = pkg_resources.get_distribution('tensorflow-detect').version
__version__ = '1.4.1'


ALLOWED_PKGS = ['tensorflow%s==%s' % (suf, __version__)
                for suf in ['', '%s-gpu']
               ]

HAS_TENSORFLOW = False

for pypkg_name in ALLOWED_PKGS:
    # exc on 404?
    dist = pkg_resources.get_distribution(pypkg_name)

    HAS_TENSORFLOW = True
    break



def _iter_installed_cudas():
    import pkgconfig

    for x in pkgconfig.list_all():
        if not x.startswith('cuda-'):
            continue

        yield x


def _install_tensorflow(detect_gpu=True, force_gpu=False, version=__version__):
    from setuptools.command import easy_install

    found_cudas = list(_iter_installed_cudas())

    log.info('Detected CUDA installations via pkg-config: %r', found_cudas)

    gpu_suffix = found_cudas and '-gpu' or ''

    pkgs = [
        'tensorflow%s==%s' % (gpu_suffix, version),
    ]

    easy_install.main(pkgs)

    return True


def _replace_module(mod='tensorflow'):
    import sys
    import importlib

    m = importlib.import_module(mod_name, package=package)
    sys.modules[mod_name] = m


def _try_tensorflow():
    pkg_resources.get_distribution
    try:
        import tensorflow
    except ImportError:
        _install_tensorflow()

