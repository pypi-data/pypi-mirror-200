import subprocess

from tests.unit_test import UnitTest


class TestBin(UnitTest):

    def test_bin_1(self):
        """manuscriptify parses command line args"""
        sp = subprocess.run(['manuscriptify', 'test', 'bin'],
                            capture_output=True)
        assert sp.stdout.decode('utf-8').strip() == 'test bin'
