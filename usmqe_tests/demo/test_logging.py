# -*- coding: utf8 -*-

"""
Demonstration of USM QE Tests Run Logging
=========================================

This is just an example of usmqe flavored pytest test cases so that one can
try how the reporting and logging works without setting up the whole test
enviroment required for actuall tests.
"""

import pytest


@pytest.fixture
def fixture_error():
    raise Exception


@pytest.fixture(params=[1, 2])
def parametrized_fixture(request):
    return [request.param]


def test_pass_one():
    pytest.check(True, 'good')


def test_pass_many():
    pytest.check(True, 'one')
    pytest.check(True, 'two')
    pytest.check(True, 'three')


@pytest.mark.parametrize("x", [1, 2, 3])
@pytest.mark.parametrize("y", ["a", "b"])
def test_pass_parametrized(x, y):
    pytest.check(len(x*y) == x)
    pytest.check(y in x*y)


def test_pass_parametrized_fixture(parametrized_fixture):
    pytest.check(len(parametrized_fixture) > 0)


def test_fail_one_check():
    pytest.check(False)


def test_fail_many_check():
    pytest.check(True, 'good')
    pytest.check(False, 'ops')
    pytest.check(False, 'doh')
    pytest.check(False, 'doh')


def test_fail_one_exception():
    # mrglog doesn't handle this
    raise Exception


def test_error_in_fixture(fixture_error):
    pytest.check(True)


def test_xfail_one():
    pytest.check(False, issue='BZ 439858')


def test_xfail_many():
    pytest.check(True, 'good')
    pytest.check(False, issue='BZ 439858')  # this failure is waived known issue


def test_fail_anyway():
    pytest.check(True, 'good')
    pytest.check(False, issue='BZ 439858')  # this failure is waived known issue
    pytest.check(False, 'this sucks')
