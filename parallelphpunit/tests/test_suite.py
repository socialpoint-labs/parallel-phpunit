from unittest import TestCase
from parallelphpunit.suite import TestFailedDetails, ReportScreen, Report
from parallelphpunit.tests import OutputTestCase
from mock import Mock


class TestFailedDetailsTestCase(TestCase):
    def test_value_object(self):
        expected_file_path = '/tmp/foo/BarTest.php'
        expected_lines = ['foo', 'bar', 'hello', 'world']

        test_failed_details = TestFailedDetails(expected_file_path, expected_lines)
        actual_file_path = test_failed_details.get_file_path()
        actual_lines = test_failed_details.get_lines()

        self.assertEqual(expected_file_path, actual_file_path)
        self.assertEqual(expected_lines, actual_lines)


class ReportScreenTestCase(OutputTestCase):
    def setUp(self):
        self._report_screen = ReportScreen()

    def test_print_dot(self):
        with self.assertOutput('\033[m.'):
            self._report_screen.print_dot()

    def test_print_failure(self):
        with self.assertOutput('\033[41m\033[37mF\033[m'):
            self._report_screen.print_failure()

    def test_print_skipped(self):
        with self.assertOutput('\033[36mS\033[m'):
            self._report_screen.print_skipped()

    def test_print_incomplete(self):
        with self.assertOutput('\033[33mI\033[m'):
            self._report_screen.print_incomplete()

    def test_print_error(self):
        with self.assertOutput('\033[31mE\033[m'):
            self._report_screen.print_error()

    def test_row(self):
        expected_output = ''
        for i in range(1, 300):
            expected_output = "%s\033[m." % expected_output
            if i % 64 == 0:
                expected_output = "%s\n" % expected_output

        with self.assertOutput(expected_output):
            for i in range(1, 300):
                self._report_screen.print_dot()

    def test_reset(self):
        expected_output = ''
        for i in range(1, 300):
            expected_output = "%s\033[m." % expected_output

        with self.assertOutput(expected_output):
            for i in range(1, 300):
                self._report_screen.print_dot()
                self._report_screen.reset()


class ReportTestCase(OutputTestCase):
    def setUp(self):
        report_screen = Mock()
        self._report = Report(report_screen)

    def test_passed(self):
        expected_output = "Time: 0 seconds\n\nPassed: 1 / 1"
        self._report.add_passed()
        with self.assertOutput(expected_output):
            self._report.display_result()

    def test_failures(self):
        expected_output = "Time: 0 seconds\n\nFails: 1 / 1"
        self._report.add_failure()
        with self.assertOutput(expected_output):
            self._report.display_result()

    def test_skipped(self):
        expected_output = "Time: 0 seconds\n\nSkipped: 1 / 1"
        self._report.add_skipped()
        with self.assertOutput(expected_output):
            self._report.display_result()

    def test_incomplete(self):
        expected_output = "Time: 0 seconds\n\nIncomplete: 1 / 1"
        self._report.add_incomplete()
        with self.assertOutput(expected_output):
            self._report.display_result()

    def test_error(self):
        expected_output = "Time: 0 seconds\n\nErrors: 1 / 1"
        self._report.add_error()
        with self.assertOutput(expected_output):
            self._report.display_result()

    def test_add_failed_details(self):
        self._report.add_failure()
        expected_file_path = '/tmp/foo/BarTest.php'
        expected_lines = ['foo', 'bar', 'hello', 'world']
        self._report.add_test_failed_details(expected_file_path, expected_lines)
        expected_output = "Time: 0 seconds\n\nFails: 1 / 1\n" \
                          "\n---------------------------------------------------------------\n\n"
        expected_output = "%s\033[41m%s\033[m\n%s" % (expected_output, expected_file_path, "\n".join(expected_lines))
        with self.assertOutput(expected_output):
            self._report.display_result()
