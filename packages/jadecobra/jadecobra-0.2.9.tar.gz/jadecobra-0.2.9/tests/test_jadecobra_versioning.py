import src.jadecobra.tester
import src.jadecobra.versioning


class TestJadeCobraVersioning(src.jadecobra.tester.TestCase):

    def test_versioning(self):
        self.assert_attributes_equal(
            src.jadecobra.versioning,
            [
                '__builtins__',
                '__cached__',
                '__doc__',
                '__file__',
                '__loader__',
                '__name__',
                '__package__',
                '__spec__',
                'get_pyproject_version',
                'git_push',
                'os',
                'pyproject',
                're',
                'read_pyproject',
                'semantic_version_pattern',
                'toolkit',
                'update_module_version',
                'update_pyproject_version',
            ]
        )

    def test_update_version(self):
        self.assertEqual(
            src.jadecobra.versioning.get_pyproject_version(
                src.jadecobra.versioning.read_pyproject()
            ),
            ('0.2.', '8'),
        )
