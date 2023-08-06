import src.jadecobra.tester
import src.jadecobra.versioning


class TestJadeCobraVersioning(src.jadecobra.tester.TestCase):

    def test_version_attributes(self):
        self.assert_attributes_equal(
            src.jadecobra.versioning,
            [
                'Version',
                '__builtins__',
                '__cached__',
                '__doc__',
                '__file__',
                '__loader__',
                '__name__',
                '__package__',
                '__spec__',
                'os',
                're',
                'toolkit',
            ]
        )

    def test_version_class_attributes(self):
        self.assert_attributes_equal(
            src.jadecobra.versioning.Version,
            [
                '__class__',
                '__delattr__',
                '__dict__',
                '__dir__',
                '__doc__',
                '__eq__',
                '__format__',
                '__ge__',
                '__getattribute__',
                '__getstate__',
                '__gt__',
                '__hash__',
                '__init__',
                '__init_subclass__',
                '__le__',
                '__lt__',
                '__module__',
                '__ne__',
                '__new__',
                '__reduce__',
                '__reduce_ex__',
                '__repr__',
                '__setattr__',
                '__sizeof__',
                '__str__',
                '__subclasshook__',
                '__weakref__',
                'get_pyproject_version',
                'git_push',
                'pyproject',
                'read_pyproject',
                'semantic_version_pattern',
                'update_module_version',
                'update_pyproject_version'
            ]
        )

    # def test_update_version(self):
    #     version = src.jadecobra.versioning.Version()
    #     self.assertEqual(
    #         version.get_pyproject_version(),
    #         ('0.3.', '2'),
    #     )
