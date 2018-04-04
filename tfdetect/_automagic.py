import atexit
import logging
import os.path
import site
import subprocess
import sys

try:
    import __builtin__
except ImportError:
    import builtins as __builtin__

log = logging.getLogger(__name__)
_pip_bin = os.path.join(sys.prefix, 'bin', 'pip')


def _openone(flist, *args):
    for p in flist:
        try:
            f = open(p, *args)
            return (p, f)
        except IOError:
            pass
    return None, None


class PipInstallError(Exception):
    pass


def _pip_install(name):
    try:
        subprocess.check_call([_pip_bin, "install", name])
    except subprocess.CalledProcessError:
        raise PipInstallError()

    return True


def _rescan_path():
    absprefix = os.path.abspath(sys.prefix)
    abspaths = [os.path.abspath(s) for s in sys.path]
    paths = [
        s for s in abspaths if s.startswith(absprefix) and
        (s.endswith('site-packages') or s.endswith('site-python'))
    ]
    site.addsitedir(paths[0])


def _iter_installed_cudas():
    import pkgconfig

    for x in pkgconfig.list_all():
        if not x.startswith('cuda-'):
            continue

        yield x


# TODO make this sane with pbr, for now hardcode?
# __version__ = pkg_resources.get_distribution(__name__).version
# __version__ = pkg_resources.get_distribution('tensorflow-detect').version
__version__ = '1.4.1'


class ImportPipInstaller(object):
    def __init__(self):
        self.realimport = __import__
        self.ignore = set()

    def __call__(self, name, *args, **kwargs):
        try:
            return self.realimport(name, *args, **kwargs)
        except ImportError:
            pass

        if name == 'tensorflow':
            log.warning('Tensorflow is required but not installed.')
            log.warning('Detecting whether we should use tensorflow gpu or cpu variant.')

            found_cudas = list(_iter_installed_cudas())

            log.info(
                'Detected CUDA installations via pkg-config: %r', found_cudas
            )

            suffix = found_cudas and '-gpu' or ''
            name = 'tensorflow%s==%s' % (suffix, __version__)

            log.warn('Installing tensorflow as detected: %r', name)

        else:
            raise ImportError(name)

        if name in self.ignore:
            raise ImportError(name)

        print("Will install module {}".format(name))

        try:
            _pip_install(name)
        except PipInstallError:
            self.ignore.add(name)
            raise ImportError(name)

        _rescan_path()

        return self.realimport(name, *args, **kwargs)


def install():
    if isinstance(__builtin__.__import__, ImportPipInstaller):
        return
    importreplacement = ImportPipInstaller()
    __builtin__.__import__ = importreplacement


@atexit.register
def uninstall():
    if isinstance(__builtin__.__import__, ImportPipInstaller):
        __builtin__.__import__ = __import__.realimport
