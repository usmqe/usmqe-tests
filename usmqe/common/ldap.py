"""
Module for functions used for LDAP

.. moduleauthor:: mkudlej
"""


from configparser import ConfigParser
import sys


def load_ldap_users_conf(conf_file):
    """
    Function returns dictionary with ldap users from given configuration file.

    Args:
        conf_file (string): path to a config file to load users from (usually
        :py:const:`usmqe.config.ldap.LDAP_USER_FILE`)

    Returns:
        dictionary: configured ldap users
    """
    ldap_users = {}
    conf = ConfigParser()
    conf.read(conf_file)
    for section in conf.sections():
        ldap_users[section] = {}
        for key, value in conf.items(section):
            if value == "None":
                value = ""
            ldap_users[section][key] = value

    return ldap_users


def main():
    """ Main function for testing util functions.
    @pylatest api/user.login_valid2
    @usmid api/user.login_valid1
    """
    print(load_ldap_users_conf(sys.argv[1]))

if __name__ == "__main__":
    main()
