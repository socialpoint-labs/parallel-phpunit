import os
import fnmatch


def find_test_case_files(test_cases_paths, test_suffix='Test.php'):
    """
    @param test_cases_paths: list
    """
    test_case_files = []
    for test_case_path in test_cases_paths:
        for root, dir_names, file_names in os.walk(test_case_path):
            for filename in fnmatch.filter(file_names, '*%s' % test_suffix):
                test_case_files.append(os.path.join(root, filename))

    return test_case_files