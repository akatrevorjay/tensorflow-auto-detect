import mock
import pytest
import logging

from tfdetect import pkg

log = logging.getLogger(__name__)

RAW_LDCONFIG_P_LINES = '''
	ld-linux-x86-64.so.2 (libc6,x86-64) => /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
	ld-linux-x32.so.2 (libc6,x32) => /libx32/ld-linux-x32.so.2
	libcurand.so.9.0 (libc6,x86-64) => /usr/local/cuda-9.0/targets/x86_64-linux/lib/libcurand.so.9.0
	libcurand.so (libc6,x86-64) => /usr/local/cuda-9.0/targets/x86_64-linux/lib/libcurand.so
'''

RAW_LDCONFIG_P_LINES_EXP = [
    dict(
        basename='ld-linux-x86-64.so.2',
        archs='libc6,x86-64',
        path='/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2',
    ),
    dict(
        archs='libc6,x32',
        basename='ld-linux-x32.so.2',
        path='/libx32/ld-linux-x32.so.2',
    ),
    dict(
        basename='libcurand.so.9.0',
        path='/usr/local/cuda-9.0/targets/x86_64-linux/lib/libcurand.so.9.0',
        archs='libc6,x86-64',
    ),
    dict(
        basename='libcurand.so',
        path='/usr/local/cuda-9.0/targets/x86_64-linux/lib/libcurand.so',
        archs='libc6,x86-64',
    ),
]

LDCONFIG_LIBS = [
    dict(
        library_name='ld-linux-x86-64',
        library_version='2',
    ),
    dict(
        library_name='ld-linux-x32',
        library_version='2',
    ),
    dict(
        library_name='libcurand',
        library_version='9.0',
    ),
    dict(
        library_name='libcurand',
        library_version=None,
    ),
]


def test_get_tf_version():
    expected = {
        '1.7': '1.7',
        '1.10+dev': '1.10',
        '1.8.1': '1.8.1',
        '1.8.1+dev': '1.8.1',
    }

    for pkg_ver, exp_tfver in expected.items():
        tfver = pkg.get_tf_version(pkg_ver)
        assert tfver == exp_tfver


def test__iter_installed_libs():
    libs = list(pkg._iter_installed_libs())
    assert libs == RAW_LDCONFIG_P_LINES_EXP


@mock.patch('subprocess.check_output', return_value=RAW_LDCONFIG_P_LINES)
def test__iter_installed_libs(m_check_output):
    libs = list(pkg._iter_installed_libs())
    assert libs == RAW_LDCONFIG_P_LINES_EXP

    m_check_output.assert_called_once()


@mock.patch('subprocess.check_output', return_value=RAW_LDCONFIG_P_LINES)
def test__search_for_installed_lib(m_check_output):
    libs = list(pkg._iter_installed_libs())
    assert libs == RAW_LDCONFIG_P_LINES_EXP

    for exp, meta in zip(RAW_LDCONFIG_P_LINES_EXP, LDCONFIG_LIBS):
        res = list(pkg._search_for_installed_lib(libs, **meta))
        log.debug('res=%r', res)
        assert exp in res


def test_detect_tensorflow_package():
    exp_cpu = 'tensorflow'
    exp_gpu = '%s-gpu' % exp_cpu

    with mock.patch.object(pkg, '_get_cuda_libs_for_tf_version',
                           return_value=[]):
        with mock.patch.object(pkg, '_has_libs', return_value=False):
            res = pkg.detect_tensorflow_package()
            res = res.rsplit('==', 1)[0]
            assert res == exp_cpu

    with mock.patch.object(pkg, '_get_cuda_libs_for_tf_version',
                           return_value=['fakelibfortruth']):
        with mock.patch.object(pkg, '_has_libs', return_value=True):
            res = pkg.detect_tensorflow_package()
            res = res.rsplit('==', 1)[0]
            assert res == exp_gpu
