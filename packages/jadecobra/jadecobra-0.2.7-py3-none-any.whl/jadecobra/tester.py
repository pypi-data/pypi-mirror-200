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
    def get_template(filepath):
        with open(f'{filepath}.template.json') as template:
            return json.load(template)

    def create_cdk_templates(self):
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
        self.assertEqual(
            self.get_template(f"cdk.out/{stack_name}"),
            self.get_template(f"tests/fixtures/{stack_name}")
        )

    def assert_attributes_equal(self, thing=None, attributes=None):
        self.assertEqual(
            sorted(dir(thing)), sorted(attributes)
        )

    @staticmethod
    def remove_dist():
        try:
            shutil.rmtree('dist')
        except FileNotFoundError:
            'already removed'


    def build_and_publish(self):
        versioning.git_push()
        self.remove_dist()
        os.system('python3 -m build')
        self.assertEqual(
            os.system('python3 -m twine upload dist/*'), 0
        )