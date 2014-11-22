from unittest import TestCase
import subprocess
import os


class AcceptanceTest(TestCase):
    def test_run_two_tests_in_parallel(self):
        current_path = os.path.dirname(os.path.realpath(__file__))
        root_path = os.path.dirname(os.path.realpath('%s/..' % current_path))
        parallel_phpunit_bin = "%s/parallel-phpunit" % root_path
        command = ["python", parallel_phpunit_bin, "--phpunit_bin", "%s/vendor/bin/phpunit" % root_path, "%s/fixtures" % current_path]
        process = subprocess.Popen(command, stdout=subprocess.PIPE)

        process.wait()

        output = process.stdout.read()
        self.assertEqual('\x1b[m.\x1b[m.\n\nTime: 0 seconds\n\nPassed: 2 / 2\n', output)