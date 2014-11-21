parallel-phpunit
================
Parallel Test Cases Runner for PHPUnit

Installation
------------
Composer
~~~~~~~~
To install with Composer, execute the following command inside your project:

.. code-block:: bash

    composer require --dev socialpoint/parallel-phpunit

After installation, the binary can be found at ``vendor/bin/parallel-phpunit``

Pip
~~~
parallel-phpunit can be installed via "pip", the Python package manager, with:

``pip install parallel-phpunit``

After installation, you can use executing ``parallel-phpunit``

Usage
-----
Usage is as follows:

.. code-block::

    parallel-phpunit [-h] [--max_concurrency MAX_CONCURRENCY]
                          [--configuration CONFIGURATION]
                          [--phpunit_bin PHPUNIT_BIN]
                          [--test_suffix TEST_SUFFIX]
                          [TestCases Dirs [TestCases Dirs ...]]

    positional arguments:
      TestCases Dirs        Directories of test cases

    optional arguments:
      -h, --help            show this help message and exit
      --max_concurrency MAX_CONCURRENCY
                            Max TestCase processing concurrency (8 by default)
      --configuration CONFIGURATION, -c CONFIGURATION
                            Read configuration from XML file
      --phpunit_bin PHPUNIT_BIN
                            phpunit bin path
      --test_suffix TEST_SUFFIX
                            phpunit test suffix (by default Test.php)
