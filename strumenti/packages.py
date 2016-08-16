#! /usr/bin/env python
# -*- coding: utf-8 -*-

"""Package Module

Utilities for managing Python packages.

.. moduleauthor:: Timothy Helton <timothy.j.helton@gmail.com>
"""

from collections import namedtuple
from datetime import datetime as dt
import glob
import subprocess
import os
import os.path as osp
import tarfile
from termcolor import colored


class Manage:
    """Class will assist with managing Python packages.

    :Attributes:

        - **log_file**: *str* name of log file
        - **outdated**: *dict* outdated packages
        - **packages**: *dict* all packages
        - **req_txt_path**: *str* path to the file containing all package \
            version requirements
        - **wheels**: *list* path to all wheels generated by installing \
            packages (this includes all dependencies)
        - **wheel_path**: *str* path to the temporary wheelhouse directory
    """
    def __init__(self):
        self.log_file = 'packages_{}.log'.format(dt.date(dt.now()))
        self._outdated = {}
        self._packages = {}
        self.req_txt_path = 'requirements.txt'
        self._wheels = []
        self.wheel_path = 'temp_wheelhouse'

    @property
    def outdated(self):
        self.list_packages(outdated=True)
        return self._outdated

    @property
    def packages(self):
        self.list_packages()
        return self._packages

    @property
    def wheels(self):
        self.get_wheels()
        return self._wheels

    def __repr__(self):
        return 'Manage()'

    def create_tar(self):
        """Create tar file of wheels."""
        with tarfile.open('{}.tar'.format(self.wheel_path), 'w:gz') as tar:
            for name in self.wheels:
                tar.add(name)

    def create_wheels(self, packages):
        """Create wheels for packages.

        :param iterable packages: names of packages to upgrade
        """
        os.makedirs(self.wheel_path, exist_ok=True)
        for pkg in packages:
            new_version = self._outdated[packages].new_ver
            with open(self.log_file, 'a') as f:
                subprocess.run(['pip', 'wheel',
                                '--wheel-dir={}'.format(self.wheel_path),
                                '{}=={}'.format(pkg, new_version)],
                               stdout=f, stderr=f)
            print(colored('{:15}{}'.format('Complete:', pkg), 'green'))

    def get_wheels(self):
        """Get the absolute path for all wheel files."""
        wheels = glob.glob('{}{}*'.format(self.wheel_path, os.sep))
        self._wheels = [osp.realpath(x) for x in wheels]

    def list_packages(self, outdated=False):
        """Get information on installed packages.

        :param bool outdated: if True only outdated packages will be retrieved
        """
        versions = namedtuple('Versions', ['old_ver', 'new_ver'])

        cmd = ['pip', 'list']
        if outdated:
            cmd.append('-o')

        execute = subprocess.run(cmd, stdout=subprocess.PIPE)
        packages = execute.stdout.decode('utf-8').splitlines()
        packages = [x.split() for x in packages]

        if outdated:
            if not packages:
                print(colored('\nAll installed packages are up to date.',
                              'green'))
            else:
                self._outdated = {x[0]: versions(x[2], x[4]) for x in packages}
        else:
            self._packages = {x[0]: x[1].strip('()') for x in packages}

    def install_packages(self, packages, upgrade=True):
        """Install Python packages.

        .. note:: The argument packages can be a list of package names as \
            strings or tuples of package names with desired versions to be \
            installed.

            - List of Strings example:
                - ['numpy', 'scipy']
            - List of Tuples example:
                - [('numpy', '1.10.4'), ('scipy', '0.16.1')]

        :param iterable packages: packages to install
        :param bool upgrade: set to True if package is already installed \
            and the version is being upgraded or False if a new package is \
            being installed
        """
        cmd = ['pip', 'install']
        if upgrade:
            cmd.append('--upgrade')

        for pkg in iter(packages):
            if isinstance(pkg, tuple):
                pkg = '{}=={}'.format(pkg[0], pkg[1])

            print(colored('\n{:10}{}'.format('Install:', pkg), 'blue'))
            cmd.append(pkg)
            with open(self.log_file, 'a') as f:
                execute = subprocess.run(cmd, stdout=f, stderr=subprocess.PIPE)

            if not execute.stderr:
                print(colored('{:10}\n'.format('Complete'), 'green'))

    def update_packages(self):
        """Update to latest version of all packages."""
        update_pkgs = self.outdated.keys()
        self.install_packages(update_pkgs)
        if update_pkgs:
            self.update_requirements()

    def update_requirements(self):
        """Update the requirements.txt file.

        .. note:: The requirements file will only be updated if the path is \
            defined in the attribute req_txt_file.
        """
        try:
            execute = subprocess.run(['pip', 'freeze'], stdout=subprocess.PIPE)
            with open(self.req_txt_path, 'w') as f:
                f.write(execute.stdout.decode('utf-8'))
            stmt = ('\nUpdated Requirements file: {}'
                    '\n').format(self.req_txt_path)
            print(colored(stmt, 'green'))
        except IOError:
            stmt = ('\nFile Not Found: {}\n'
                    'Requirements File Not Updated\n').format(self.req_txt_path)
            print(colored(stmt, 'red'))


if __name__ == '__main__':
    p = Manage()
    p.update_packages()
