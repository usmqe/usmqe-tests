import pytest
from usmqe.base.application.implementations.web_ui import ViaWebUI
import copy
import time
from wait_for import TimedOutError
import datetime

from usmqe.api.tendrlapi import user as tendrlapi_user
# from usmqe.api.tendrlapi.common import login, logout
from usmqe.base.application import Application
from usmqe.usmqeconfig import UsmConfig
from usmqe import usmssh, usmmail


LOGGER = pytest.get_logger('ui_user_testing', module=True)
CONF = UsmConfig()


@pytest.mark.author("ebondare@redhat.com")
@pytest.mark.parametrize("receive_alerts", [True, False])
@pytest.mark.happypath
def test_alerting(application, receive_alerts, valid_normal_user_data):
    """
    Create normal user with email notifications switched on or off.
    Check that alerts appear in the mailbox according to notification settings.
    """
    """
    :step:
      Change admin's email to avoid collision.
    :result:
      Admin's email is changed
    """

    # create a user with the email address configured in ansible playbook
    new_data = {"email": "alerting_test" + str(receive_alerts) + "@ya.ru",
                "password": CONF.config["usmqe"]["password"],
                "confirm_password": CONF.config["usmqe"]["password"]}
    application.collections.users.edit_logged_in_user(new_data)
    """
    :step:
      Create normal user with notifications switched on or off.
    :result:
      Normal user is created
    """
    user = application.collections.users.create(
        user_id=valid_normal_user_data["username"],
        name=valid_normal_user_data["name"],
        email="root@" + CONF.inventory.get_groups_dict()["usm_client"][0],
        notifications_on=receive_alerts,
        password=valid_normal_user_data["password"],
        role=valid_normal_user_data["role"]
    )
    """
    :step:
      Stop glusterd on one of the cluster nodes.
    :result:
      After some time alerts are generated
    """

    start_time = datetime.datetime.now().timestamp()
    SSH = usmssh.get_ssh()
    host = CONF.config["usmqe"]["cluster_member"]
    stop_cmd = "systemctl stop glusterd"
    time.sleep(90)
    retcode, stdout, stderr = SSH[host].run(stop_cmd)
    if retcode != 0:
        raise OSError(stderr)
    """
    :step:
      Restart glusterd.
    :result:
      After some time alerts disappear
    """

    restart_cmd = "systemctl restart glusterd"
    time.sleep(90)
    retcode, stdout, stderr = SSH[host].run(restart_cmd)
    if retcode != 0:
        raise OSError(stderr)
    stop_time = datetime.datetime.now().timestamp()
    """
    :step:
      Gather e-mails that came after glusterd was stopped and check if there were any.
    :result:
      There should be some or no e-mails according to user settings.
    """

    messages = usmmail.get_msgs_by_time(start_timestamp=start_time,
                                              end_timestamp=stop_time)
    LOGGER.debug("Selected messages count: {}".format(len(messages)))
    alert_received = False
    for message in messages:
        LOGGER.debug("Message date: {}".format(message['Date']))
        LOGGER.debug("Message subject: {}".format(message['Subject']))
        LOGGER.debug("Message body: {}".format(message.get_payload(decode=True)))
        if message['Subject'].count("]"):
            alert_received = True
    if receive_alerts:
        pytest.check(alert_received)
    else:
        pytest.check(not alert_received)
    user.delete()
