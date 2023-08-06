import subprocess
import unittest

from . import toolkit
from . import versioning


class TestCase(unittest.TestCase):

    maxDiff = None

    def create_cdk_templates(self):
        '''Create CloudFormation using CDK with presets'''
        result = toolkit.run_in_shell(
            (
                'cdk ls '
                '--no-version-reporting '
                '--no-path-metadata '
                '--no-asset-metadata'
            )
        )
        self.assertEqual(result.returncode, 0)

    def assert_cdk_templates_equal(self, stack_name):
        '''Check if stack_name in cdk.out folder and tests/fixtures are the same'''
        self.assertEqual(
            toolkit.read_json(f"cdk.out/{stack_name}"),
            toolkit.read_json(f"tests/fixtures/{stack_name}")
        )

    def assert_attributes_equal(self, thing=None, attributes=None):
        '''Check that the given attributes match the attributes of thing'''
        self.assertEqual(
            sorted(dir(thing)), sorted(attributes)
        )