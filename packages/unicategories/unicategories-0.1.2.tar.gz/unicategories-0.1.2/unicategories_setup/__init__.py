"""unicategories setuptools tools."""

import contextlib
import sys

from setuptools.command.install import install as BaseInstall
from setuptools.dist import Distribution as BaseDistribution

from .cache import install_cache


class install(BaseInstall):
    """Unicategories install command class."""

    sub_commands = BaseInstall.sub_commands + [
        ('install_cache', None),
        ]


class Distribution(BaseDistribution):
    """Unicategories distribution class."""

    default_cmdclass = {
        'install': install,
        'install_cache': install_cache,
        }

    package_content = None

    def __init__(self, attrs):
        """Initialize."""
        cmdclass = self.default_cmdclass.copy()
        cmdclass.update(attrs.get('cmdclass', ()))
        attrs['cmdclass'] = cmdclass

        if sys.version_info < (3, ):
            BaseDistribution.__init__(self, attrs)
        else:
            super(Distribution, self).__init__(attrs)


@contextlib.contextmanager
def sys_path(path):
    """Add path to sys.path, thread-unsafe context manager."""
    if path in sys.path:
        yield
    else:
        sys.path.insert(0, path)
        yield
        sys.path.remove(path)
