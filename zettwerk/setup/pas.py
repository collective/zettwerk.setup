# -*- coding: utf-8 -*-


def set_pas_session_cookie_name(portal, name):
    """ set the session cookie name to the given name. """
    portal.acl_users.session.manage_changeProperties(cookie_name=name)


def set_pas_session_cookie_timeout(portal, timeout):
    """ set the timeout (in seconds) for the session cookie.

        Setting the timeout to 0 will disable the timeout check

    """
    portal.acl_users.session.manage_changeProperties(timeout=timeout)
