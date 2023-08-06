"""unicategories setuptools install_cache command."""

import os
import os.path
from distutils import log
from distutils.core import Command


class install_cache(Command):
    """Distutils subcommand generating and installing package cache."""

    description = 'Generate and install package cache'

    user_options = [
        ('install-dir=', 'd', "directory to install to"),
        ]

    def initialize_options(self):
        """Initialize command options."""
        self.install_dir = None
        self.outfiles = []

    def finalize_options(self):
        """Initialize command options (final step)."""
        self.set_undefined_options(
            'install_lib',
            ('install_dir', 'install_dir'),
            )
        self.package_content = self.distribution.package_content

    def run(self):
        """Generate install files."""
        log.info('Generating install files')
        for package, files in self.package_content.items():
            for path, fnc in files.items():
                base = os.path.dirname(path)
                if base and not os.path.exists(base):
                    os.makedirs(base)
                abspath = os.path.join(self.install_dir, package, path)
                print(abspath)
                if not self.dry_run:
                    fnc(abspath)
                self.outfiles.append(abspath)

    def get_inputs(self):
        """Get command inputs (stub)."""
        return []

    def get_outputs(self):
        """Get command output files."""
        return self.outfiles
