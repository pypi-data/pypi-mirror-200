import re
import os

from . import toolkit

def pyproject():
    return 'pyproject.toml'

def read_pyproject():
    with open(pyproject()) as file:
        return file.read()

def semantic_version_pattern():
    return r'version\s+=\s+"(\d+[.]\d+[.])(\d+)"'

def get_pyproject_version(text):
    '''Get version from pyproject.toml'''
    return re.search(
        semantic_version_pattern(),
        text
    ).group(1, 2)

def update_pyproject_version():
    '''Update version in pyproject.toml'''
    text = read_pyproject()
    version, patch = get_pyproject_version(text)
    toolkit.write_file(
        filepath=pyproject(),
        data=re.sub(
            semantic_version_pattern(),
            f'version = "{version}{int(patch)+1}"',
            text
        )
    )

def update_module_version():
    '''Update Module Version'''
    text = read_pyproject()
    version, patch = get_pyproject_version(text)
    toolkit.write_file(
        filepath='src/jadecobra/__init__.py',
        data=f"__version__ = {version}{int(patch)+1}",
    )

def git_push():
    '''Update version for project'''
    try:
        update_pyproject_version()
        update_module_version()
    except FileNotFoundError:
        pass
    finally:
        os.system(f'git commit -am "{toolkit.get_commit_message()}"')
        os.system('git push')