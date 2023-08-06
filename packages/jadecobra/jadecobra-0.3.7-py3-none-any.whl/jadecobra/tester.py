import json
import os
import shutil
import subprocess
import unittest

from . import versioning
from . import toolkit


class TestCase(unittest.TestCase):

    maxDiff = None

    @staticmethod
    def read_json(filepath):
        '''Return a dictionary from a json file'''
        with open(f'{filepath}.template.json') as template:
            return json.load(template)

    def create_cdk_templates(self):
        '''Create CloudFormation using CDK with presets'''
        result = toolkit.time_it(
            (
                'cdk ls '
                '--no-version-reporting '
                '--no-path-metadata '
                '--no-asset-metadata'
            ),
            function=subprocess.run,
            description=f'cdk ls',
            shell=True,
            capture_output=True,
        )
        print(result.stderr.decode())
        print(result.stdout.decode())
        self.assertEqual(result.returncode, 0)

    def assert_cdk_templates_equal(self, stack_name):
        '''Check if stack_name in cdk.out folder and tests/fixtures are the same'''
        self.assertEqual(
            self.read_json(f"cdk.out/{stack_name}"),
            self.read_json(f"tests/fixtures/{stack_name}")
        )

    def assert_attributes_equal(self, thing=None, attributes=None):
        '''Check that the given attributes match the attributes of thing'''
        self.assertEqual(
            sorted(dir(thing)), sorted(attributes)
        )

    @staticmethod
    def remove_dist():
        '''Remove Dist folder for new distribution'''
        try:
            shutil.rmtree('dist')
        except FileNotFoundError:
            'already removed'

    def build_and_publish(self):
        '''Build the python distribution and upload to pypi'''
        versioning.Version().git_push()
        self.remove_dist()
        os.system('python3 -m build')
        self.assertEqual(
            os.system('python3 -m twine upload dist/*'), 0
        )