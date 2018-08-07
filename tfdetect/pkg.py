#!/usr/bin/env python
import os
import logging
import subprocess
import re

from tfdetect import utils
from setuptools import find_packages, setup

log = logging.getLogger(__name__)

TRUTHY_STRINGS = ['true', 'True', 't', '1']

LDCONFIG_P_EXEC = ['ldconfig', '-Np']
LDCONFIG_P_RE = re.compile(
    r'^\t(?P<basename>[^\s]+) \((?P<archs>[^\)]+)\) => (?P<path>[^\s]+)$'
)

cuda_libs = {
    '9.0':
        dict(cublas='9.0', cudnn='7', cufft='9.0', curand='9.0', cudart='9.0'),
}

cuda_version_map = {
    '1.7': cuda_libs['9.0'],
    '1.8': cuda_libs['9.0'],
    '1.9': cuda_libs['9.0'],
    '1.10': cuda_libs['9.0'],
}


def get_version(fn='VERSION'):
    with open(fn, 'r') as fh:
        version = fh.readlines()[0].rstrip('\n')
    return version


def get_tf_version(version=get_version):
    if callable(version):
        version = version()

    tf_version = version.rsplit('+', 1)[0]
    return tf_version


def _iter_pkgconfig_cudas():
    import pkgconfig

    try:
        pkgs = pkgconfig.list_all()
    except Exception as exc:
        return

    for x in pkgs:
        if not x.startswith('cuda-'):
            continue

        yield x


def _iter_installed_libs(cmd=LDCONFIG_P_EXEC, cmd_line_re=LDCONFIG_P_RE):
    raw = subprocess.check_output(cmd)
    lines = raw.splitlines()

    for line in lines[1:]:
        line = utils.ensure_decoded_text(line)
        line = line.rstrip('\n')

        m = cmd_line_re.match(line)
        if not m:
            log.warning(
                'Could not parse %r output line: %r',
                LDCONFIG_P_EXEC,
                line,
            )
            continue

        yield m.groupdict()


def _search_for_installed_lib(
        library_name,
        library_version=None,
        cmd=LDCONFIG_P_EXEC,
        cmd_line_re=LDCONFIG_P_RE.match,
):
    log.info('Searching for library %r==%r', library_name, library_version)

    g = _iter_installed_libs(cmd=cmd, cmd_line_re=cmd_line_re)

    for lib in g:
        base = lib['basename']

        found = []

        found.append(base.startswith(library_name))

        if library_version is not None:
            found.append(base.endswith('.%s' % library_version))

        found = all(found)

        if found:
            yield lib


def _get_cuda_libs_for_tf_version(tf_version):
    for prefix, libs in cuda_version_map.items():
        if tf_version.startswith(prefix):
            return libs


def _has_libs(libs):
    log.info('Looking for libraries %r', libs)

    for lib_name, lib_version in libs.items():
        found = _search_for_installed_lib(lib_name, lib_version)
        if not found:
            return False

    return True


def detect_tensorflow_package(tf_version=get_tf_version):
    if callable(tf_version):
        tf_version = tf_version()

    log.info(
        'Detecting whether we should require tensorflow gpu or cpu variant.'
    )

    use_gpu = []

    force_gpu = os.environ.get('TENSORFLOW_FORCE_GPU')
    force_gpu = force_gpu in TRUTHY_STRINGS
    use_gpu.append(force_gpu)

    pkgconfig_cudas = list(_iter_pkgconfig_cudas())
    use_gpu.append(pkgconfig_cudas)

    libs = _get_cuda_libs_for_tf_version(tf_version)
    print(libs)
    if libs:
        has_libs = _has_libs(libs)
        print(has_libs)

    use_gpu = any(use_gpu)

    if use_gpu:
        log.warning(
            'Detected CUDA installation; requiring GPU tensorflow variant.',
            pkgconfig_cudas,
        )
    else:
        log.warning(
            'Did NOT detect CUDA installation via pkg-config; requiring CPU tensorflow variant.',
        )

    suffix = use_gpu and '-gpu' or ''
    name = 'tensorflow%s==%s' % (suffix, tf_version)

    return name
