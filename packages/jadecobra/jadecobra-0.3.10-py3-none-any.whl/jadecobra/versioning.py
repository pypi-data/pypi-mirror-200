import re
import shutil

from . import toolkit


class Version(object):

    def __init__(self):
        self.text = self.read_pyproject()
        self.version, self.patch = self.get_pyproject_version()
        self.new_version = f"{self.version}{int(self.patch)+1}"

    @staticmethod
    def pyproject():
        return 'pyproject.toml'

    @staticmethod
    def semantic_version_pattern():
        return r'version\s+=\s+"(\d+[.]\d+[.])(\d+)"'

    def read_pyproject(self):
        '''Return contents of file'''
        with open(self.pyproject()) as file:
            return file.read()

    def get_pyproject_version(self):
        '''Get version from pyproject.toml'''
        return re.search(
            self.semantic_version_pattern(),
            self.text
        ).group(1, 2)

    def update_pyproject_version(self):
        '''Update version in pyproject.toml'''
        toolkit.write_file(
            filepath=self.pyproject(),
            data=re.sub(
                self.semantic_version_pattern(),
                f'version = "{self.new_version}"',
                self.text
            )
        )

    def update_module_version(self):
        '''Update Module Version'''
        toolkit.write_file(
            filepath='src/jadecobra/__init__.py',
            data=f'__version__ = "{self.new_version}"',
        )

    @staticmethod
    def remove_dist():
        '''Remove Dist folder for new distribution'''
        try:
            shutil.rmtree('dist')
        except FileNotFoundError:
            'already removed'

    def update(self):
        self.remove_dist()
        self.update_pyproject_version()
        self.update_module_version()