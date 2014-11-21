from unittest import TestCase
import sys
from StringIO import StringIO
import os.path
from discover import DiscoveringTestLoader


def get_tests():  # pragma: no cover
    start_dir = os.path.dirname(__file__)
    test_loader = DiscoveringTestLoader()
    return test_loader.discover(start_dir, pattern="test_*.py")


class OutputTestCase(TestCase):
    def assertOutput(self, expected_output):
        return _AssertOutputContext(expected_output, self)


class _AssertOutputContext():
    """
    Usage example:
        class ExampleTestCase(OutputTestCase):
            def test_example(self):
                with self.assertOutput('Hello\nWorld'):
                    print('Hello')
                    print('World')
    """
    def __init__(self, expected_output, test_case):
        """
        @param expected_output: str
        @param test_case: unittest.TestCase
        """
        self._expected_output = expected_output
        self._test_case = test_case

    def __enter__(self):
        self._saved_stdout = sys.stdout
        self._out = StringIO()
        sys.stdout = self._out

    def __exit__(self, *args):
        actual_output = self._out.getvalue().strip()
        try:
            self._test_case.assertEquals(self._expected_output, actual_output)
        finally:
            sys.stdout = self._saved_stdout
