import src.jadecobra
import src.jadecobra.tester
import src.jadecobra.toolkit
import src.jadecobra.versioning
import os


class TestJadeCobra(src.jadecobra.tester.TestCase):

    def test_jadecobra(self):
        self.assert_attributes_equal(
            src.jadecobra,
            []
        )

    def test_tester_attributes(self):
        self.assert_attributes_equal(
            src.jadecobra.tester,
            [
                'TestCase',
                '__builtins__',
                '__cached__',
                '__doc__',
                '__file__',
                '__loader__',
                '__name__',
                '__package__',
                '__spec__',
                'json',
                'os',
                'shutil',
                'subprocess',
                'toolkit',
                'unittest',
                'versioning'
            ]
        )

    def test_tester_test_case_attributes(self):
        self.assert_attributes_equal(
            src.jadecobra.tester.TestCase,
            [
                '__call__',
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
                '_addExpectedFailure',
                '_addUnexpectedSuccess',
                '_baseAssertEqual',
                '_callCleanup',
                '_callSetUp',
                '_callTearDown',
                '_callTestMethod',
                '_classSetupFailed',
                '_class_cleanups',
                '_deprecate',
                '_diffThreshold',
                '_formatMessage',
                '_getAssertEqualityFunc',
                '_truncateMessage',
                'addClassCleanup',
                'addCleanup',
                'addTypeEqualityFunc',
                'assertAlmostEqual',
                'assertAlmostEquals',
                'assertCountEqual',
                'assertDictContainsSubset',
                'assertDictEqual',
                'assertEqual',
                'assertEquals',
                'assertFalse',
                'assertGreater',
                'assertGreaterEqual',
                'assertIn',
                'assertIs',
                'assertIsInstance',
                'assertIsNone',
                'assertIsNot',
                'assertIsNotNone',
                'assertLess',
                'assertLessEqual',
                'assertListEqual',
                'assertLogs',
                'assertMultiLineEqual',
                'assertNoLogs',
                'assertNotAlmostEqual',
                'assertNotAlmostEquals',
                'assertNotEqual',
                'assertNotEquals',
                'assertNotIn',
                'assertNotIsInstance',
                'assertNotRegex',
                'assertNotRegexpMatches',
                'assertRaises',
                'assertRaisesRegex',
                'assertRaisesRegexp',
                'assertRegex',
                'assertRegexpMatches',
                'assertSequenceEqual',
                'assertSetEqual',
                'assertTrue',
                'assertTupleEqual',
                'assertWarns',
                'assertWarnsRegex',
                'assert_',
                'assert_attributes_equal',
                'assert_cdk_templates_equal',
                'build_and_publish',
                'countTestCases',
                'create_cdk_templates',
                'debug',
                'defaultTestResult',
                'doClassCleanups',
                'doCleanups',
                'enterClassContext',
                'enterContext',
                'fail',
                'failIf',
                'failIfAlmostEqual',
                'failIfEqual',
                'failUnless',
                'failUnlessAlmostEqual',
                'failUnlessEqual',
                'failUnlessRaises',
                'failureException',
                'id',
                'longMessage',
                'maxDiff',
                'read_json',
                'remove_dist',
                'run',
                'setUp',
                'setUpClass',
                'shortDescription',
                'skipTest',
                'subTest',
                'tearDown',
                'tearDownClass'
            ]
        )

    def test_toolkit(self):
        self.assert_attributes_equal(
            src.jadecobra.toolkit,
            [
                '__builtins__',
                '__cached__',
                '__doc__',
                '__file__',
                '__loader__',
                '__name__',
                '__package__',
                '__spec__',
                'datetime',
                'delete',
                'delimiter',
                'error',
                'file_exists',
                'get_commit_message',
                'header',
                'log_performance',
                'logger',
                'make_dir',
                'os',
                'pathlib',
                'time',
                'time_it',
                'to_camel_case',
                'write_config',
                'write_file'
            ]
        )

    def test_to_camel_case(self):
        self.assertEqual(
            src.jadecobra.toolkit.to_camel_case('abc-def-hij'),
            'AbcDefHij'
        )

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
            ('0.2.', '7'),
        )

    def test_published_version_is_test_version(self):
        os.system('pip install jadecobra')
        import jadecobra
        self.assertEqual(
            jadecobra.__version__,
            src.jadecobra.__version__
        )
