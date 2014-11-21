import os
from setuptools import setup, find_packages


base_dir = os.path.dirname(os.path.abspath(__file__))

setup(
    name="parallel-phpunit",
    version="1.0.0",
    description="Parallel Test Cases Runner for PHPUnit",
    long_description="\n\n".join([
        open(os.path.join(base_dir, "README.rst"), "r").read(),
    ]),
    url="https://github.com/socialpoint/parallel-phpunit",
    author="Felix Carmona",
    packages=find_packages(exclude=('parallelphpunit.tests', 'parallelphpunit.tests.*')),
    zip_safe=False,
    entry_points = {
         'console_scripts': [
             'parallel-phpunit = parallelphpunit:main',
         ],
    },
    test_suite="parallelphpunit.tests.get_tests"
)
