Demonstration of USM QE Tests Run Logging
=========================================

This is just an example of usmqe flavored pytest test cases so that one can
try how the reporting and logging works without setting up the whole test
enviroment required for actuall tests.

To run this demo, go into the root directory of usmqe-test repository and
assuming you have all requirements installed (eg. in current virtualenv), run::

    $ python -m pytest usmqe_tests/demo/test_logging.py -v

Note that for this demo to work, you need to have the test environment
configured, as described in more detail in `Test Configuration`_ document.

This way, you would be able to see standard pytest output::

    ============================================ test session starts =============================================
    platform linux -- Python 3.6.3, pytest-3.6.1, py-1.5.3, pluggy-0.6.0 -- /opt/rh/rh-python36/root/usr/bin/python
    cachedir: .pytest_cache
    rootdir: /home/usmqe/usmqe-tests, inifile: pytest.ini
    plugins: ansible-playbook-0.3.0
    collected 17 items

    usmqe_tests/demo/test_logging.py::test_pass_one PASSED                                                 [  5%]
    usmqe_tests/demo/test_logging.py::test_pass_many PASSED                                                [ 11%]
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[a-1] PASSED                                   [ 17%]
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[a-2] PASSED                                   [ 23%]
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[a-3] PASSED                                   [ 29%]
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[b-1] PASSED                                   [ 35%]
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[b-2] PASSED                                   [ 41%]
    usmqe_tests/demo/test_logging.py::test_pass_parametrized[b-3] PASSED                                   [ 47%]
    usmqe_tests/demo/test_logging.py::test_pass_parametrized_fixture[1] PASSED                             [ 52%]
    usmqe_tests/demo/test_logging.py::test_pass_parametrized_fixture[2] PASSED                             [ 58%]
    usmqe_tests/demo/test_logging.py::test_fail_one_check FAILED                                           [ 64%]
    usmqe_tests/demo/test_logging.py::test_fail_many_check FAILED                                          [ 70%]
    usmqe_tests/demo/test_logging.py::test_fail_one_exception FAILED                                       [ 76%]
    usmqe_tests/demo/test_logging.py::test_error_in_fixture ERROR                                          [ 82%]
    usmqe_tests/demo/test_logging.py::test_xfail_one xfail                                                 [ 88%]
    usmqe_tests/demo/test_logging.py::test_xfail_many xfail                                                [ 94%]
    usmqe_tests/demo/test_logging.py::test_fail_anyway FAILED                                              [100%]

    =================================================== ERRORS ===================================================
    __________________________________ ERROR at setup of test_error_in_fixture ___________________________________

        @pytest.fixture
        def fixture_error():
    >       raise Exception
    E       Exception

    usmqe_tests/demo/test_logging.py:17: Exception
    ------------------------------------------- Captured stdout setup --------------------------------------------

    [09:28:30,524] :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    [09:28:30,524] Test error in fixture started
    ================================================== FAILURES ==================================================
    ____________________________________________ test_fail_one_check _____________________________________________
    usmqe_tests/demo/test_logging.py:47: AssumptionFailure
            pytest.check(False)

    ------------------------------------------------------------
    Failed Assumptions: 1, Passed Assumption: 0, Waived Assumption: 0
    ------------------------------------------- Captured stdout setup --------------------------------------------

    [09:28:30,471] :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    [09:28:30,472] Test fail one check started
    -------------------------------------------- Captured stdout call --------------------------------------------
    [09:28:30,477] [ FAIL     ] main_test:: usmqe_tests/demo/test_logging.py:47: AssumptionFailure
            pytest.check(False)

    ------------------------------------------ Captured stdout teardown ------------------------------------------
    [09:28:30,478] Test fail one check duration  : 0s
    [09:28:30,478] Test fail one check assertions: 0 good, 1 bad
    [09:28:30,479] Test fail one check result    : FAIL
    [09:28:30,479] :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    ____________________________________________ test_fail_many_check ____________________________________________
    usmqe_tests/demo/test_logging.py:52: AssumptionFailure
            ops

    usmqe_tests/demo/test_logging.py:53: AssumptionFailure
            doh

    usmqe_tests/demo/test_logging.py:54: AssumptionFailure
            doh
    ------------------------------------------------------------
    Failed Assumptions: 3, Passed Assumption: 1, Waived Assumption: 0
    ------------------------------------------- Captured stdout setup --------------------------------------------

    [09:28:30,481] :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    [09:28:30,481] Test fail many check started
    -------------------------------------------- Captured stdout call --------------------------------------------
    [09:28:30,486] [ PASS     ] main_test:: usmqe_tests/demo/test_logging.py:51: AssumptionPassed
            good
    [09:28:30,490] [ FAIL     ] main_test:: usmqe_tests/demo/test_logging.py:52: AssumptionFailure
            ops
    [09:28:30,495] [ FAIL     ] main_test:: usmqe_tests/demo/test_logging.py:53: AssumptionFailure
            doh
    [09:28:30,499] [ FAIL     ] main_test:: usmqe_tests/demo/test_logging.py:54: AssumptionFailure
            doh
    ------------------------------------------ Captured stdout teardown ------------------------------------------
    [09:28:30,500] Test fail many check duration  : 0s
    [09:28:30,500] Test fail many check assertions: 1 good, 3 bad
    [09:28:30,501] Test fail many check result    : FAIL
    [09:28:30,501] :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    __________________________________________ test_fail_one_exception ___________________________________________

        def test_fail_one_exception():
            # mrglog doesn't handle this
    >       raise Exception
    E       Exception

    usmqe_tests/demo/test_logging.py:59: Exception
    ------------------------------------------- Captured stdout setup --------------------------------------------

    [09:28:30,503] :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    [09:28:30,503] Test fail one exception started
    ------------------------------------------ Captured stdout teardown ------------------------------------------
    [09:28:30,520] [ ERROR    ] main_test:: Exception
    [09:28:30,521] Test fail one exception duration  : 0s
    [09:28:30,521] Test fail one exception assertions: 0 good, 0 bad
    [09:28:30,522] Test fail one exception result    : ERROR
    [09:28:30,522] :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    ______________________________________________ test_fail_anyway ______________________________________________
    usmqe_tests/demo/test_logging.py:78: AssumptionFailure
            this sucks
    ------------------------------------------------------------
    Failed Assumptions: 1, Passed Assumption: 1, Waived Assumption: 1
    ------------------------------------------- Captured stdout setup --------------------------------------------

    [09:28:30,557] :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    [09:28:30,557] Test fail anyway started
    -------------------------------------------- Captured stdout call --------------------------------------------
    [09:28:30,562] [ PASS     ] main_test:: usmqe_tests/demo/test_logging.py:76: AssumptionPassed
            good
    [09:28:30,566] [ WAIVE    ] main_test:: usmqe_tests/demo/test_logging.py:77: AssumptionFailure
            pytest.check(False, issue='BZ 439858')  # this failure is waived known issue

            Known issue: BZ 439858
    [09:28:30,567] [ DEBUG    ] main_test:: Add issue: 'BZ 439858'
    [09:28:30,571] [ FAIL     ] main_test:: usmqe_tests/demo/test_logging.py:78: AssumptionFailure
            this sucks
    ------------------------------------------ Captured stdout teardown ------------------------------------------
    [09:28:30,572] Test fail anyway duration  : 0s
    [09:28:30,572] Test fail anyway assertions: 1 good, 1 bad
    [09:28:30,573] Test fail anyway result    : FAIL
    [09:28:30,573] :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    [09:28:30,573] :::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::::
    [09:28:30,574] =======================================================================================
    [09:28:30,574] =======================================================================================
    [09:28:30,574] Test-case[s] Summary: (17 found)
    [09:28:30,575] ---------------------------------------------------------------------------------------
    [09:28:30,575] PASS  pass one                                :  #tests:1     #fails:0     desc.:""
    [09:28:30,575] PASS  pass many                               :  #tests:3     #fails:0     desc.:""
    [09:28:30,575] PASS  pass parametrized[a-1]                  :  #tests:2     #fails:0     desc.:""
    [09:28:30,576] PASS  pass parametrized[a-2]                  :  #tests:2     #fails:0     desc.:""
    [09:28:30,576] PASS  pass parametrized[a-3]                  :  #tests:2     #fails:0     desc.:""
    [09:28:30,576] PASS  pass parametrized[b-1]                  :  #tests:2     #fails:0     desc.:""
    [09:28:30,576] PASS  pass parametrized[b-2]                  :  #tests:2     #fails:0     desc.:""
    [09:28:30,577] PASS  pass parametrized[b-3]                  :  #tests:2     #fails:0     desc.:""
    [09:28:30,577] PASS  pass parametrized fixture[1]            :  #tests:1     #fails:0     desc.:""
    [09:28:30,577] PASS  pass parametrized fixture[2]            :  #tests:1     #fails:0     desc.:""
    [09:28:30,578] FAIL  fail one check                          :  #tests:1     #fails:1     desc.:""
    [09:28:30,578] FAIL  fail many check                         :  #tests:4     #fails:3     desc.:""
    [09:28:30,578] ERROR fail one exception                      :  #tests:0     #fails:0     desc.:""
    [09:28:30,578] ERROR error in fixture                        :  #tests:0     #fails:0     desc.:""
    [09:28:30,579] PASS  xfail one                               :  #tests:0     #fails:0     desc.:""
    [09:28:30,579] PASS  xfail many                              :  #tests:1     #fails:0     desc.:""
    [09:28:30,579] FAIL  fail anyway                             :  #tests:2     #fails:1     desc.:""
    [09:28:30,579] =======================================================================================
    [09:28:30,580] List of known issues:
    [09:28:30,580] ---------------------------------------------------------------------------------------
    [09:28:30,580] BZ 439858
    [09:28:30,580] =======================================================================================
    [09:28:30,581] =======================================================================================
    [09:28:30,581] Test-Cases Summary   #TOTAL: 17    #PASSED: 12   #FAILED: 3    #ERRORS: 2
    [09:28:30,581] Test Summary : ERROR #TOTAl: 29    #PASSED: 21   #FAILED: 5    #ERRORS: 2   #WAIVES: 3
    [09:28:30,581] Test name    : /home/usmqe/usmqe-tests
    [09:28:30,582] Duration     : 0:00:00.497478
    [09:28:30,582] Test on      : CentOS Linux release 7.5.1804 (Core) x86_64
    [09:28:30,582] =======================================================================================
    [09:28:30,583] =======================================================================================
    [09:28:30,583] Test finished: 09:28:30,573953
    ========================== 4 failed, 10 passed, 2 xfailed, 1 error in 0.37 seconds ===========================

Full mrglog_ log report is placed into ``logs/testlog.txt`` file::

    $ tail logs/testlog.txt
    [09:28:30,580] =======================================================================================
    [09:28:30,581] =======================================================================================
    [09:28:30,581] Test-Cases Summary   #TOTAL: 17    #PASSED: 12   #FAILED: 3    #ERRORS: 2
    [09:28:30,581] Test Summary : ERROR #TOTAl: 29    #PASSED: 21   #FAILED: 5    #ERRORS: 2   #WAIVES: 3
    [09:28:30,581] Test name    : /home/usmqe/usmqe-tests
    [09:28:30,582] Duration     : 0:00:00.497478
    [09:28:30,582] Test on      : CentOS Linux release 7.5.1804 (Core) x86_64
    [09:28:30,582] =======================================================================================
    [09:28:30,583] =======================================================================================
    [09:28:30,583] Test finished: 09:28:30,573953


.. _`Test Configuration`: https://github.com/usmqe/usmqe-tests/blob/master/docs/test_configuration.rst
.. _mrglog: https://github.com/ltrilety/mrglog
