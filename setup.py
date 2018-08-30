#!/usr/bin/env python

import logging

from setuptools import find_packages, setup
from tfdetect.pkg import detect_tensorflow_package, get_version

log = logging.getLogger(__name__)


_tf_pip_name = detect_tensorflow_package()
log.warn('Installing tensorflow as detected: %r', _tf_pip_name)


with open('README.md', 'r') as fh:
    readme = fh.read()


conf = dict(
    name='tensorflow-detect',
    summary=
    'Automatically install CPU or GPU tensorflow determined by looking for a CUDA installation.',
    author='Trevor Joynson',
    author_email='github@skywww.net',
    long_description=readme,
    license='GPL',
    packages=find_packages(),
    version=get_version(),
    setup_requires=['setuptools>=17.1'],
    tests_require=['pytest', 'mock', 'coverage', 'coveralls'],
    install_requires=[_tf_pip_name],
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
