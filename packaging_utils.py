import glob
import itertools
import os

try:
    from pip._internal.req import parse_requirements
    from pip._internal.download import PipSession
except ImportError:
    from pip.req import parse_requirements
    from pip.download import PipSession


def setup_requirements(
        patterns=[
            'requirements.txt', 'requirements/*.txt', 'requirements/*.pip'
        ],
        combine=True):
    """
    Parse a glob of requirements and return a dictionary of setup() options.
    Create a dictionary that holds your options to setup() and update it using this.
    Pass that as kwargs into setup(), viola

    Any files that are not a standard option name (ie install, tests, setup) are added to extras_require with their
    basename minus ext. An extra key is added to extras_require: 'all', that contains all distinct reqs combined.

    Keep in mind all literally contains `all` packages in your extras.
    This means if you have conflicting packages across your extras, then you're going to have a bad time.
    (don't use all in these cases.)

    If you're running this for a Docker build, set `combine=True`.
    This will set `install_requires` to all distinct reqs combined.

    Example:

    >>> import setuptools
    >>> _conf = dict(
    ...     name='mainline',
    ...     version='0.0.1',
    ...     description='Mainline',
    ...     author='Trevor Joynson <github@trevor.joynson,io>',
    ...     url='https://trevor.joynson.io',
    ...     namespace_packages=['mainline'],
    ...     packages=setuptools.find_packages(),
    ...     zip_safe=False,
    ...     include_package_data=True,
    ... )
    >>> _conf.update(setup_requirements())
    >>> setuptools.setup(**_conf)

    :param str pattern: Glob pattern to find requirements files
    :param bool combine: Set True to set install_requires to extras_require['all']
    :return dict: Dictionary of parsed setup() options
    """
    session = PipSession()

    # Handle setuptools insanity
    key_map = {
        'requirements': 'install_requires',
        'install': 'install_requires',
        'tests': 'tests_require',
        'setup': 'setup_requires',
    }
    ret = {v: set() for v in key_map.values()}
    extras = ret['extras_require'] = {}
    all_reqs = set()

    files = [glob.glob(pat) for pat in patterns]
    files = itertools.chain(*files)

    for full_fn in files:
        # Parse
        reqs = {
            str(r.req)
            for r in parse_requirements(full_fn, session=session)
            # Must match env marker, eg:
            #   yarl ; python_version >= '3.0'
            if r.match_markers()
        }
        all_reqs.update(reqs)

        # Add in the right section
        fn = os.path.basename(full_fn)
        barefn, _ = os.path.splitext(fn)
        key = key_map.get(barefn)

        if key:
            ret[key].update(reqs)
            extras[key] = reqs

        extras[barefn] = reqs

    if 'all' not in extras:
        extras['all'] = list(all_reqs)

    if combine:
        extras['install'] = ret['install_requires']
        ret['install_requires'] = list(all_reqs)

    def _listify(dikt):
        ret = {}

        for k, v in dikt.items():
            if isinstance(v, set):
                v = list(v)
            elif isinstance(v, dict):
                v = _listify(v)
            ret[k] = v

        return ret

    ret = _listify(ret)

    return ret


__all__ = ['setup_requirements']

if __name__ == '__main__':
    reqs = setup_requirements()
    print(reqs)
