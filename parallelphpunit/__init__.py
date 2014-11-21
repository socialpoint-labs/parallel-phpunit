#!/usr/bin/env python
import sys
import argparse
from parallelphpunit.runner import TestRunner
import os


def main():
    parser = argparse.ArgumentParser(description='Runs PhpUnit TestCases in parallel')
    parser.add_argument('test_cases_dirs', metavar='TestCases Dirs', type=str, nargs='*', default=[os.getcwd()], help='Directories of test cases')
    parser.add_argument('--max_concurrency', type=int, default=8, help='Max TestCase processing concurrency (8 by default)')
    parser.add_argument('--configuration', '-c', type=str, help='Read configuration from XML file')
    parser.add_argument('--phpunit_bin', default='phpunit', type=str, help='phpunit bin path')
    parser.add_argument('--test_suffix', default='Test.php', type=str, help='phpunit test suffix (by default Test.php)')

    args = parser.parse_args()

    test_runner = TestRunner(args.test_cases_dirs, args.max_concurrency, args.configuration, args.phpunit_bin, args.test_suffix)
    is_successful = test_runner.run()

    if not is_successful:
        sys.exit(2)

if __name__ == "__main__":
    main()
