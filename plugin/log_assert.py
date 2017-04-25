# -*- coding: utf8 -*-

# The MIT License (MIT)
#
# Copyright (c) 2015, Brian Okken
# Copyright (c) 2016, Luboš Tříletý <ltrilety@redhat.com>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.


import inspect
import os
import os.path

import pytest
import mrglog

try:
    from py.io import saferepr
except ImportError:
    saferepr = repr

CHECKLOGGER = None


""" pytest conditional assert """


class No_log_filter(object):
    """ filter all messages with LOG_LEVEL """

    def filter(self, logRecord):
        """ return False for LOG_LEVEL messages, True otherwise """
        return logRecord.levelno != mrglog.LOG_LEVEL


def pytest_namespace():
    """
    Add tracking lists to the pytest namespace, so we can
    always access it, as well as the 'check' function itself.

    :return: Dictionary of name: values added to the pytest namespace.
    """

    def check(expr, msg='', hard=False, issue=None):
        """
        Checks the expression, if it's false, add it to the
        list of failed assumptions. Also, add the locals at each failed
        assumption, if showlocals is set.

        :param expr: Expression to 'assert' on.
        :param msg: Message to display
        :param hard: if test should continue if the assertion fails
        :param issue: known issue, log WAIVE
        :return: None
        """
        if CHECKLOGGER is None:
            set_logger()
        # get filename, line, and context
        (frame, filename, line, funcname, contextlist) = \
            inspect.stack()[1][0:5]
        filename = os.path.relpath(filename)
        context = contextlist[0].lstrip() if not msg else msg
        if not expr:
            # format entry
            entry = "{filename}:{line}: "\
                    "AssumptionFailure\n\t{context}".format(**locals())
            # add entry
            if pytest.config.option.showlocals:
                # Debatable whether we should display locals for
                # every failed assertion, or just the final one.
                # I'm defaulting to per-assumption, just because the vars
                # can easily change between assumptions.
                pretty_locals = ["%-10s = %s" % (name, saferepr(val))
                                 for name, val in frame.f_locals.items()]
                pytest._assumption_locals.append(pretty_locals)
            if issue is not None:
                entry = '{entry}\n\tKnown issue: {issue}'.format(**locals())
                CHECKLOGGER.waived(entry)
                CHECKLOGGER.add_issue(issue)
            else:
                CHECKLOGGER.failed(entry)
            if hard:
                # fail the test
                pytest.fail(entry)
        else:
            # format entry
            entry = "{filename}:{line}: "\
                    "AssumptionPassed\n\t{context}".format(**locals())
            # track passed ones too
            # add entry
            CHECKLOGGER.passed(entry)

    return {'_assumption_locals': [],
            'check': check,
            'get_logger': get_logger,
            'set_logger': set_logger}


@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    """
    Check if the test failed, if it didn't fail, and there are
    failed assumptions, fail the test & output the assumptions as the longrepr.

    If the test already failed, then just add in failed assumptions
    to a new section in the longrepr.

    :param item:
    :param call:
    :return:
    """
    if CHECKLOGGER is None:
        set_logger()
    outcome = yield
    report = outcome.get_result()
    # add an error to mrglog module if needed
    try:
        message = report.longrepr.reprcrash.message
        CHECKLOGGER.error(message)
    except AttributeError:
        pass
    failed_assumptions = CHECKLOGGER.act_test['fail']
    passed_assumptions = CHECKLOGGER.act_test['pass']
    waived_assumptions = CHECKLOGGER.act_test['waive']
    assumption_locals = getattr(pytest, "_assumption_locals", [])
    evalxfail = getattr(item, '_evalxfail', None)
    if call.when == "call" and (failed_assumptions or waived_assumptions):
        if (evalxfail and evalxfail.wasvalid() and evalxfail.istrue()) or\
           (waived_assumptions and not failed_assumptions):
            report.outcome = "skipped"
            if evalxfail and evalxfail.wasvalid() and evalxfail.istrue():
                report.wasxfail = evalxfail.getexplanation()
            else:
                report.wasxfail = "some waived assumptions present"
        else:
            summary = 'Failed Assumptions: {0}, '\
                'Passed Assumption: {1}, '\
                'Waived Assumption: {2}'.format(
                    len(failed_assumptions),
                    len(passed_assumptions),
                    len(waived_assumptions))
            if report.longrepr:
                # Do we want to have the locals displayed here as well?
                # I'd say no, because the longrepr
                # would already be displaying locals.
                report.sections.append((
                    summary, "\n".join(failed_assumptions)))
            else:
                if assumption_locals:
                    assume_data = zip(
                        failed_assumptions + waived_assumptions,
                        assumption_locals)
                    longrepr = [
                        "{0}\n{1}\n\n".format(assumption, "\n".join(flocals))
                        for assumption, flocals in assume_data]
                else:
                    longrepr = ["\n\n".join(failed_assumptions)]
                longrepr.append("-" * 60)
                longrepr.append(summary)
                report.longrepr = '\n'.join(longrepr)
            if failed_assumptions:
                report.outcome = "failed"

    if hasattr(pytest, "_failed_assumptions"):
        del pytest._failed_assumptions[:]
    if hasattr(pytest, "_passed_assumptions"):
        del pytest._assumption_locals[:]
    if hasattr(pytest, "_waived_assumptions"):
        del pytest._assumption_locals[:]
    if hasattr(pytest, "_assumption_locals"):
        del pytest._assumption_locals[:]


def get_logger(*args, **kwargs):
    if 'verbose_lvl' not in kwargs:
        kwargs['verbose_lvl'] = 0
    if 'output' not in kwargs:
        kwargs['output'] = ['std', 'txt']
    logger = mrglog.get_logger(*args, **kwargs)
    for handler in logger.handlers:
        # logging.FileHandler is probably inherited from logging.StreamHandler
        # hence isinstance is not working properly
        # if isinstance(handler, logging.StreamHandler):
        if 'logging.StreamHandler' in str(handler):
            handler.addFilter(No_log_filter())
    return logger


def set_logger(logger=None):
    global CHECKLOGGER
    if logger is not None:
        CHECKLOGGER = logger
    else:
        CHECKLOGGER = get_logger("usm_assume", module=True)
