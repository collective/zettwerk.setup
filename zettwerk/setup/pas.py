# -*- coding: utf-8 -*-


def set_pas_session_cookie_name(portal, name):
    """ set the session cookie name to the given name. """
    portal.acl_users.session.manage_changeProperties(cookie_name=name)
