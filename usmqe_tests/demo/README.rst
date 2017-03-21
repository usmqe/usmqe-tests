Demonstration of USM QE Tests Run Logging
=========================================

This is just an example of usmqe flavored pytest test cases so that one can
try how the reporting and logging works without setting up the whole test
enviroment required for actuall tests.

To run this demo, go into the root directory of usmqe-test repository and
assuming you have all requirements installed (eg. in current virtualenv), run::

    $ python -m pytest usmqe_tests/demo/test_logging.py -v

This way, you would be able to see standard pytest output::

    platform linux -- Python 3.5.3, pytest-3.0.6, py-1.4.32, pluggy-0.4.0 -- /home/martin/projects/usmqe-tests/.env/bin/python
    cachedir: .cache
    rootdir: /home/martin/projects/usmqe-tests, inifile: pytest.ini
    plugins: ansible-playbook-0.3.0
    collected 17 items

    usmqe_tests/demo/test_logging.py::test_pass_one PASSED
    usmqe_tests/demo/test_logging.py::test_pass_many PASSED
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[a-1] PASSED
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[a-2] PASSED
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[a-3] PASSED
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[b-1] PASSED
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[b-2] PASSED
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[b-3] PASSED
    usmqe_tests/demo/test_logging.py::test_pass_parametrized_fixture[1] PASSED
    usmqe_tests/demo/test_logging.py::test_pass_parametrized_fixture[2] PASSED
    usmqe_tests/demo/test_logging.py::test_fail_one_check FAILED
    usmqe_tests/demo/test_logging.py::test_fail_many_check FAILED
    usmqe_tests/demo/test_logging.py::test_fail_one_exception FAILED
    usmqe_tests/demo/test_logging.py::test_error_in_fixture ERROR
    usmqe_tests/demo/test_logging.py::test_xfail_one xfail
    usmqe_tests/demo/test_logging.py::test_xfail_many xfail
    usmqe_tests/demo/test_logging.py::test_fail_anyway FAILED

Full mrglog log report is placed into ``logs/testlog.txt`` file::

    $ tail logs/testlog.txt
    [09:44:27,569] =======================================================================================
    [09:44:27,569] =======================================================================================
    [09:44:27,570] Test-Cases Summary   #TOTAL: 17    #PASSED: 12   #FAILED: 3    #ERRORS: 2
    [09:44:27,570] Test Summary : ERROR #TOTAl: 29    #PASSED: 21   #FAILED: 5    #ERRORS: 2   #WAIVES: 3
    [09:44:27,570] Test name    : home/martin/projects/usmqe-tests
    [09:44:27,570] Duration     : 0:00:00.133387
    [09:44:27,570] Test on      : Fedora release 25 (Twenty Five) x86_64
    [09:44:27,570] =======================================================================================
    [09:44:27,570] =======================================================================================
    [09:44:27,570] Test finished: 09:44:27,567594
