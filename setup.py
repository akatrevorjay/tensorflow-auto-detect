#!/usr/bin/env python

import atexit
import logging
import os.path
import site
import subprocess
import sys

import pkg_resources
import versioneer
from setuptools import setup, find_packages

try:
    import __builtin__
except ImportError:
    import builtins as __builtin__

log = logging.getLogger(__name__)

__version__ = versioneer.get_version()

tf_version = __version__.rsplit('+', 1)[0]


def _iter_installed_cudas():
    import pkgconfig

    for x in pkgconfig.list_all():
        if not x.startswith('cuda-'):
            continue

        yield x


def detect_tensorflow_package(version=tf_version):
    log.warning('Tensorflow is required but not installed.')
    log.warning(
        'Detecting whether we should use tensorflow gpu or cpu variant.'
    )

    found_cudas = list(_iter_installed_cudas())

    if found_cudas:
        log.info(
            'Detected CUDA installations via pkg-config (found_cudas=%r); using GPU tensorflow variant.',
            found_cudas,
        )
    else:
        log.info(
            'Did NOT detect any CUDA installations via pkg-config; using CPU tensorflow variant.',
        )

    suffix = found_cudas and '-gpu' or ''
    name = 'tensorflow%s==%s' % (suffix, version)

    return name


tf_pip_install_name = detect_tensorflow_package()
log.warn('Installing tensorflow as detected: %r', tf_pip_install_name)

conf = dict(
    name='tf-detect',
    summary=
    'Automatically install CPU or GPU tensorflow determined by looking for a CUDA installation.',
    author='Trevor Joynson',
    author_email='github@skywww.net',
    license='GPL',
    packages=find_packages(),
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    setup_requires=['setuptools>=17.1'],
    install_requires=[tf_pip_install_name],
    keywords=['tensorflow', 'wtf'],
    classifier=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Information Technology',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development',
        'Topic :: Software Development :: Libraries',
    ],
)

if __name__ == '__main__':
    setup(**conf)
