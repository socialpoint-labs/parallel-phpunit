from parallelphpunit.files import find_test_case_files
import subprocess
import re
from parallelphpunit.suite import Report, ReportScreen
from os.path import abspath


class TestRunner:
    ANSI_ESCAPE = re.compile(r'\x1b[^m]*m')

    def __init__(
            self,
            test_cases_path,
            max_concurrency,
            configuration_path=None,
            phpunit_bin='phpunit',
            test_suffix='Test.php'
    ):
        self._test_cases_path = test_cases_path
        self._max_concurrency = max_concurrency
        self._configuration_path = None if configuration_path is None else abspath(configuration_path)
        self._phpunit_bin = phpunit_bin
        self._test_suffix = test_suffix

    def run(self):
        report = Report(ReportScreen())

        if self._configuration_path is not None:
            print("Configuration read from %s\n" % self._configuration_path)

        remaining_test_case_files = find_test_case_files(self._test_cases_path, self._test_suffix)
        processes = set()
        while remaining_test_case_files or processes:
            if remaining_test_case_files and len(processes) < self._max_concurrency:
                test_case_file_path = remaining_test_case_files.pop()

                command = [self._phpunit_bin]
                if self._configuration_path:
                    command += ['-c', self._configuration_path]
                command.append(test_case_file_path)

                process = subprocess.Popen(command, stdout=subprocess.PIPE)
                process.test_case = test_case_file_path
                processes.add(process)

            finished_processes = []
            for process in processes:
                if process.poll() is not None:
                    finished_processes.append(process)
                    output = process.stdout.read()
                    output_data = output.split('\n')[4:]
                    if output_data:
                        test_case_dots = output_data[0]

                        uncolored_dots = self.ANSI_ESCAPE.sub('', test_case_dots)
                        for dot_type in uncolored_dots:
                            if dot_type == '.':
                                report.add_passed()
                            if dot_type == 'F':
                                report.add_failure()
                            elif dot_type == 'S':
                                report.add_skipped()
                            elif dot_type == 'I':
                                report.add_incomplete()
                            elif dot_type == 'E':
                                report.add_error()

                        if process.returncode != 0:
                            errors_info = output_data[4:-3]
                            report.add_test_failed_details(process.test_case, errors_info)
                    else:
                        report.add_failure()
                        report.add_test_failed_details(process.test_case, [output])

            processes.difference_update(finished_processes)

        report.display_result()

        return not report.has_failed_tests()
