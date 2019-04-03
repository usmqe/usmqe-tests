"""
Module for working with email alerts.

.. moduleauthor:: ebondare

Usage::

    import usmqe.usmmail

    # ...get all  messages from /var/mail/root on the client machine
    # Return a string

    messages = usmqe.usmmail.get_client_mail()

    # ...get messages from /var/mail/root on the client machine
    # that came within the specified time interval
    # Return a mailbox object

    messages = usmqe.usmmail.get_msgs_by_time(start_timestamp, end_timestamp)
"""


import pytest
import usmqe.usmssh
import mailbox
import email.utils
import os
import tempfile
from usmqe.usmqeconfig import UsmConfig


LOGGER = pytest.get_logger('usmmail', module=True)
CONF = UsmConfig()


def create_mailbox_file(filename='mbox_file', content=''):
    tmpdirname = tempfile.mkdtemp()
    mbox_file_path = os.path.join(tmpdirname, filename)
    with open(mbox_file_path, 'w') as f:
        f.write(content)
    return mbox_file_path


def get_client_mail(host=None, user="root"):
    """
    Read mail from /var/mail/{user} on the specified machine (by default
    client machine). Return the contents of the mailbox as a string
    """
    SSH = usmqe.usmssh.get_ssh()
    if host is None:
        host = CONF.inventory.get_groups_dict()["usm_client"][0]
    cat_mail_log_cmd = "cat /var/mail/" + user
    retcode, stdout, stderr = SSH[host].run(cat_mail_log_cmd)
    LOGGER.debug("Return code of 'cat /var/mail/{}': {}".format(user, retcode))
    LOGGER.debug("Stderr of cat: ".format(stderr.decode()))
    if retcode != 0 and stderr.decode().count('No such file') > 0:
        return ''
    if retcode != 0:
        raise OSError(stderr)
    return stdout.decode()


def get_msgs_by_time(
        start_timestamp=None, end_timestamp=None, host=None, user="root"):
    """
    Get all the messages from /var/mail/{user} on the client machine or
    the specified machine.
    Choose the ones that came within the specified time interval.

    Return a mailbox object.
    """
    # Pretend we have a Date header; get the date from the Received header
    client_mail = str(get_client_mail(host=host, user=user)).replace(
        ';', '\nDate:')

    mailbox_instance = mailbox.mbox(create_mailbox_file(content=client_mail))
    relevant_messages = mailbox.mbox(create_mailbox_file())
    # Choose the messages
    for message in mailbox_instance.values():
        msg_date = email.utils.parsedate_tz(message['Date'])
        msg_timestamp = email.utils.mktime_tz(msg_date)
        if (start_timestamp is None or start_timestamp < msg_timestamp) and \
           (end_timestamp is None or end_timestamp > msg_timestamp):
            LOGGER.debug("Message date: {}".format(message['Date']))
            LOGGER.debug("Message subject: {}".format(message['Subject']))
            LOGGER.debug("Message body: {}".format(
                message.get_payload(decode=True)))
            LOGGER.debug("Message timestamp: {}".format(msg_timestamp))
            relevant_messages.add(message)

    return relevant_messages
