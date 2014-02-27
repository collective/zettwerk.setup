# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.component import getMultiAdapter

from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import IPortletManager


def cleanup_default_plone(portal, remove_default_workflows=False):
    """ remove portlets, objects and other not needed stuff """
    if 'front-page' in portal:
        portal.manage_delObjects(['front-page'])
    if 'Members' in portal:
        portal.manage_delObjects(['Members'])

    # Setup right portlets: Disable news/events, enable worklist
    rightHandler = getUtility(IPortletManager,
                              name=u'plone.rightcolumn',
                              context=portal)
    rightPortlets = getMultiAdapter((portal, rightHandler,),
                                    IPortletAssignmentMapping,
                                    context=portal)
    if u'news' in rightPortlets:
        del rightPortlets[u'news']
    if 'news' in portal:
        portal.manage_delObjects('news')

    if u'events' in rightPortlets:
        del rightPortlets[u'events']
    if 'events' in portal:
        portal.manage_delObjects('events')

    if remove_default_workflows:
        for wf in ['comment_review_workflow',
                   'folder_workflow',
                   'intranet_folder_workflow',
                   'intranet_workflow',
                   'one_state_workflow',
                   'plone_workflow',
                   'simple_publication_workflow']:
            if wf in portal.portal_workflow:
                portal.portal_workflow.manage_delObjects([wf])
