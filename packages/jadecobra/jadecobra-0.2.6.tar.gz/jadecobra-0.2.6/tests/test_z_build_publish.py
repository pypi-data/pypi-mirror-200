import jadecobra.toolkit
import os


class TestZBuildDeploy(jadecobra.toolkit.TestCase):

    def test_z_build_and_publish(self):
        self.build_and_publish()
        os.system('pip install jadecobra')