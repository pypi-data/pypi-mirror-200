import importlib
import src.jadecobra.tester
import src.jadecobra.versioning
import src.jadecobra.toolkit
import os

class TestZBuildDeploy(src.jadecobra.tester.TestCase):

    version = src.jadecobra.versioning.Version()

    @staticmethod
    def get_latest_published_version():
        library = 'jadecobra'
        print(f'installing latest version of {library}...')
        for command in (
            f'uninstall {library} -y',
            f'install {library}',
        ):
            os.system(f'pip {command}')

    def assert_published_version_is_source_version(self):
        import jadecobra
        self.assertEqual(
            jadecobra.__version__,
            src.jadecobra.__version__
        )
        self.assertEqual(
            jadecobra.__version__,
            self.version.current_pyproject_version
        )

    def test_z_published_version_is_test_version(self):
        self.get_latest_published_version()
        self.assert_published_version_is_source_version()
        import jadecobra
        try:
            self.assertEqual(
                src.jadecobra.toolkit.publish(True),
                0
            )
        except AssertionError:
            try:
                self.version.update()
            except FileNotFoundError:
                pass
            finally:
                self.assertEqual(
                    src.jadecobra.toolkit.publish(True),
                    0
                )
                self.get_latest_published_version()
                importlib.reload(jadecobra)
                self.assertEqual(
                    jadecobra.__version__,
                    src.jadecobra.__version__
                )
                self.assertEqual(
                    jadecobra.__version__,
                    self.version.current_pyproject_version
                )