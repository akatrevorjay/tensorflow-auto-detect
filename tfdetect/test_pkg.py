import pytest
import mock

from tfdetect import pkg

RAW_LDCONFIG_P_LINES = '''
	ld-linux-x86-64.so.2 (libc6,x86-64) => /lib/x86_64-linux-gnu/ld-linux-x86-64.so.2
	ld-linux-x32.so.2 (libc6,x32) => /libx32/ld-linux-x32.so.2
'''

RAW_LDCONFIG_P_LINES_EXP = [
    {
        'basename': 'ld-linux-x86-64.so.2',
        'archs': 'libc6,x86-64',
        'path': '/lib/x86_64-linux-gnu/ld-linux-x86-64.so.2'
    },
    {
        'archs': 'libc6,x32',
        'basename': 'ld-linux-x32.so.2',
        'path': '/libx32/ld-linux-x32.so.2'
    },
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
    assert libs


@mock.patch('subprocess.check_output', return_value=RAW_LDCONFIG_P_LINES)
def test__search_for_installed_lib(m_check_output):
    libs = list(pkg._iter_installed_libs())
    assert libs == RAW_LDCONFIG_P_LINES_EXP

    m_check_output.assert_called_once()


@mock.patch('subprocess.check_output', return_value=RAW_LDCONFIG_P_LINES)
def test__search_for_installed_lib(m_check_output):
    libs = list(pkg._iter_installed_libs())
    assert libs == RAW_LDCONFIG_P_LINES_EXP

    res = list(
        pkg._search_for_installed_lib(
            library_name='ld-linux-x86-64', library_version='2', libs=libs
        )
    )
    exp = [RAW_LDCONFIG_P_LINES_EXP[0]]
    assert res == exp
    assert len(res) == 1

    res = list(
        pkg._search_for_installed_lib(library_name='ld-linux-x32', libs=libs)
    )
    exp = [RAW_LDCONFIG_P_LINES_EXP[1]]
    assert res == exp
    assert len(res) == 1


def test_detect_tensorflow_package():
    exp_cpu = 'tensorflow'
    exp_gpu = '%s-gpu' % exp_cpu

    res = pkg.detect_tensorflow_package()
    res = res.rsplit('==', 1)[0]
    assert res == exp_cpu

    with mock.patch.object(pkg, '_get_cuda_libs_for_tf_version',
                           return_value=['fakelib']):
        with mock.patch.object(pkg, '_has_libs', return_value=True):
            res = pkg.detect_tensorflow_package()
            res = res.rsplit('==', 1)[0]
            assert res == exp_gpu
