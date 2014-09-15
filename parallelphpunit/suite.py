import sys
from time import time


class TestFailedDetails:
    def __init__(self, file_path, lines):
        """
        @param file_path: str
        @param lines: list or tuple
        """
        self._file_path = file_path
        self._lines = lines

    def get_file_path(self):
        return self._file_path

    def get_lines(self):
        return self._lines


class ReportScreen:
    def __init__(self, max_elements_in_a_row=64):
        self._elements_in_the_current_row = 0
        self._max_elements_in_a_row = max_elements_in_a_row

    def print_dot(self):
        self._print_element('\033[m.')

    def print_failure(self):
        self._print_element('\033[41m\033[37mF\033[m')

    def print_skipped(self):
        self._print_element('\033[36mS\033[m')

    def print_incomplete(self):
        self._print_element('\033[33mI\033[m')

    def print_error(self):
        self._print_element('\033[31mE\033[m')

    def _print_element(self, element):
        sys.stdout.write(element)
        self._elements_in_the_current_row += 1

        if self._elements_in_the_current_row == self._max_elements_in_a_row:
            print("")
            self._elements_in_the_current_row = 0

    def reset(self):
        self._elements_in_the_current_row = 0


class Report:
    def __init__(self, report_screen):
        """
        @param report_screen: ReportScreen
        """
        self._passed = 0
        self._skipped = 0
        self._incomplete = 0
        self._failures = 0
        self._errors = 0
        self._report_screen = report_screen
        self._tests_failed_details = []
        self._starting_time = int(time())

    def add_passed(self):
        self._passed += 1
        self._report_screen.print_dot()

    def add_skipped(self):
        self._skipped += 1
        self._report_screen.print_skipped()

    def add_incomplete(self):
        self._incomplete += 1
        self._report_screen.print_incomplete()

    def add_failure(self):
        self._failures += 1
        self._report_screen.print_failure()

    def add_error(self):
        self._errors += 1
        self._report_screen.print_error()

    def add_test_failed_details(self, file_path, lines):
        test_failed_details = TestFailedDetails(file_path, lines)
        self._tests_failed_details.append(test_failed_details)

    def has_failed_tests(self):
        return self._failures or self._errors

    def display_result(self):
        elapsed_time = self._human_format_duration(int(time()) - self._starting_time)
        print("\n\nTime: %s\n" % elapsed_time)

        total = self._passed + self._skipped + self._incomplete + self._failures + self._errors
        if self._failures:
            print("Fails: %s / %s" % (self._failures, total))
        if self._errors:
            print("Errors: %s / %s" % (self._errors, total))
        if self._skipped:
            print("Skipped: %s / %s" % (self._skipped, total))
        if self._incomplete:
            print("Incomplete: %s / %s" % (self._incomplete, total))
        if self._passed:
            print("Passed: %s / %s" % (self._passed, total))

        if self._tests_failed_details:
            print("\n---------------------------------------------------------------\n")
            for test_failed in self._tests_failed_details:
                print('\033[41m%s\033[m' % test_failed.get_file_path())
                for line in test_failed.get_lines():
                    print(line)

    @staticmethod
    def _human_format_duration(seconds):
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)

        minutes = long(minutes)
        hours = long(hours)

        duration = []
        if hours > 0:
            duration.append('%d hour' % hours + 's' * (hours != 1))
        if minutes > 0:
            duration.append('%d minute' % minutes + 's' * (minutes != 1))
        if seconds > 0:
            duration.append('%d second' % seconds + 's' * (seconds != 1))
        else:
            return '0 seconds'

        return ' '.join(duration)
