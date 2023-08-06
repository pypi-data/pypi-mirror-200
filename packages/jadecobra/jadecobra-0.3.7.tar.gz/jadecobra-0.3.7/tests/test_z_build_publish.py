import src.jadecobra.tester
import os

class TestZBuildDeploy(src.jadecobra.tester.TestCase):

    def test_z_build_and_publish(self):
        self.build_and_publish()

    def test_update_version(self):
        version = src.jadecobra.versioning.Version()
        self.assertEqual(
            version.get_pyproject_version(),
            ('0.3.', '2'),
        )

    def test_z_published_version_is_test_version(self):
        os.system('pip install jadecobra')
        import jadecobra
        self.assertEqual(
            jadecobra.__version__,
            src.jadecobra.__version__
        )