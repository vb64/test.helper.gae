"""
Module for environment setup and tests runner
"""
import os
import sys
import logging
from unittest import TestLoader, TextTestRunner


def path_setup():
    cur_dir = os.getcwd()
    sys.path.insert(1, os.path.join(cur_dir, 'tests', 'gae'))
    # raw_input(sys.path)

def main():
    """
    Tests runner
    """
    path_setup()
    sys.path.insert(1, os.getcwd())
    import tester_coverage

    verbose = 1
    suite = None
    loader = TestLoader()
    buf = True
    log_level = logging.NOTSET

    if len(sys.argv) > 1:
        arg1 = sys.argv[1]

        if arg1 == 'verbose':
            verbose = 2
            suite = loader.discover('tests')
            log_level = logging.CRITICAL
        elif arg1 == 'combine':
            return tester_coverage.combine(dest_dir=".", data_dir="tests")
        elif arg1 == 'clean':
            return tester_coverage.clean("tests")
        elif arg1 == 'increment':
            tester_coverage.is_increment = True
            suite = loader.discover('tests')
        else:
            lst = arg1.split('.')
            tester_coverage.clean_coverage_data(
              os.path.join(*lst[:-1]),
              ".coverage.{}".format(lst[-1])
            )
            suite = loader.loadTestsFromNames([sys.argv[1]])
            buf = False
            tester_coverage.is_increment = True
    else:
        tester_coverage.clean('tests')
        suite = loader.discover('tests')
        log_level = logging.CRITICAL

    logging.disable(log_level)
    sys.exit(
      0 if TextTestRunner(verbosity=verbose, buffer=buf).run(suite).wasSuccessful() else 1
    )


if __name__ == '__main__':
    main()
