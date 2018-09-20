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
import time
import email.utils
import os


LOGGER = pytest.get_logger('usmmail', module=True)


def get_client_mail():
    """
    Read mail from /var/mail/root on client machine.
    Return the contents of the mailbox as a string
    """
    SSH = usmqe.usmssh.get_ssh()
    host = usmqe.inventory.role2hosts("usm_client")[0]
    cat_mail_log_cmd = "cat /var/mail/root"
    retcode, stdout, stderr = SSH[host].run(cat_mail_log_cmd)
    if retcode != 0:
        raise OSError(stderr)
    return stdout.decode()


def get_msgs_by_time(start_timestamp=None, end_timestamp=None):
    """
    Get all the messages from /var/mail/root on the client machine.
    Choose the ones that came within the specified time interval.

    Return a mailbox object.
    """
    # Pretend we have a Date header; get the date from the Received header
    client_mail = get_client_mail().replace(';', '\nDate:')
    with open('mailbox_file', 'w') as f:
        f.write(client_mail)
    mailbox_instance = mailbox.mbox('mailbox_file')
    relevant_messages = mailbox.mbox('relevant_messages_mailbox')

    # Choose the messages
    for message in mailbox_instance.values():
        LOGGER.debug("Message date: {}".format(message['Date']))
        LOGGER.debug("Message subject: {}".format(message['Subject']))
        LOGGER.debug("Message body: {}".format(message.get_payload(decode=True)))
        msg_date_tuple = email.utils.parsedate(message['Date'])
        LOGGER.debug("Message date cleared: {}".format(msg_date_tuple))
        # email.utils.parsedate doesn't get the timezone correctly
        # parse "Wed, 19 Sep 2018 14:41:22 +0200 (CEST)" for the number of hours to adjust
        msg_timezone_int = int(message['Date'].split(' ')[5][:3])
        LOGGER.debug("Message timezone: {}".format(msg_timezone_int))
        msg_timestamp = time.mktime(msg_date_tuple) - msg_timezone_int * 60 * 60
        LOGGER.debug("Message timestamp: {}".format(msg_timestamp))
        if (start_timestamp is None or start_timestamp < msg_timestamp) and \
           (end_timestamp is None or end_timestamp > msg_timestamp):
            relevant_messages.add(message)

    # Clean up
    os.remove('mailbox_file')
    os.remove('relevant_messages_mailbox')
    return relevant_messages
