#!/usr/bin/env python

import logging

from setuptools import find_packages, setup

log = logging.getLogger(__name__)


def get_version(fn='VERSION'):
    with open(fn, 'r') as fh:
        version = fh.readlines()[0].rstrip('\n')
    return version


def get_tf_version(version=get_version):
    if callable(version):
        version = version()

    tf_version = version.rsplit('+', 1)[0]
    return tf_version


tf_version = get_tf_version()


def _iter_installed_cudas():
    import pkgconfig

    # I think it's best to fail hard here when pkg-config is not available,
    # otherwise the user may get an unexpected version, hence no try/except here.

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
    name='tensorflow-detect',
    summary=
    'Automatically install CPU or GPU tensorflow determined by looking for a CUDA installation.',
    author='Trevor Joynson',
    author_email='github@skywww.net',
    license='GPL',
    packages=find_packages(),
    version=get_version(),
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
