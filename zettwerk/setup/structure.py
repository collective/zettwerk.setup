# -*- coding: utf-8 -*-

import transaction

from Products.CMFCore.utils import getToolByName
from zope.component import getMultiAdapter
from zope.component import getUtility

from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import ILocalPortletAssignmentManager


def handle_structure(portal, structure):
    u"""Aktualisiert die Inhalte-Struktur, indem bestehende Objekte angepasst
    oder nicht vorhandene neu erzeugt werden.

    Dazu wird die Strukturdefinition ``structure`` ausgewertet.
    Sie besteht aus einer Liste von Einträgen.
    Jeder Eintrag entspricht einem Objekt.

    Ein Eintrag ist ein Dictionary-Objekt mit Schlüssel/Werte-Paaren.

    Beliebige Ebenen möglich
    Die zweite Ebene ist unter dem Schlüssel ``sub_structure`` abzulegen und
    ist gleich aufgebaut.

    Folgende Schlüssel werden unterstützt:

    ** erforderlich **

    * 'id': id of the object
    * 'portal_type': portal_type of the object

    ** optional **

    * 'title': title of the object
    * 'description': description of the object
    * 'exclude': True/False to exclude from nav
    * 'default': True/False to set as default page of context
    * 'wf_transition': a workflow transition to call
    * 'disable_portlets': True/False to disable portlets
    * 'local_roles': list with tuples of local roles to assign
    * 'disable_acquired_local_roles': True/False to disable (False defaults)
    * 'sub_structure': Strukturdefinition der nächstunteren Ebene
    * 'text': content
    * 'layout': view name of the default view
    * 'enable_next_previous': bool for next/previous navigation on folders
    """

    def rek(parent, structure):
        for e, entry in enumerate(structure):
            added_obj = _handle_structure_entry(parent, entry)
            parent.moveObjectToPosition(entry['id'], e)

            sub_structure = entry.get('sub_structure', [])
            rek(added_obj, sub_structure)

    parent = portal
    rek(parent, structure)


def _handle_structure_entry(context, entry):
    """ create the object if needed. entry is a dict with some keys to
    control extra stuff.

    Beschreibung der Felder siehe :func:`handle_structure`.

    returns the created obj
    """
    if entry['id'] in context:
        obj = getattr(context, entry['id'])
    else:
        context.invokeFactory(entry['portal_type'],
                              entry['id'])
        obj = getattr(context, entry['id'])

    transaction.savepoint()
    obj.setTitle(entry.get('title', ''))
    obj.setDescription(entry.get('description', ''))
    if entry.get('text', '') and obj.schema.get('text') is not None:
        obj.setText(entry.get('text'))

    if entry.get('binary', '') and obj.portal_type == 'Image':
        obj.setImage(entry.get('binary'))

    exclude_from_nav = entry.get('exclude')
    if exclude_from_nav is not None:
        obj.setExcludeFromNav(exclude_from_nav)

    if entry.get('default'):
        context.saveDefaultPage(entry['id'])

    if entry.get('layout'):
        obj.setLayout(entry['layout'])

    if entry.get('enable_next_previous') is True:
        obj.setNextPreviousEnabled(True)

    if entry.get('wf_transition'):
        wf_tool = getToolByName(context, name='portal_workflow')
        ## we must check if this is a valid transition
        ## for example if the target state is already reached
        wfs = wf_tool.getWorkflowsFor(obj)
        for wf in wfs:
            if wf.isActionSupported(obj, entry['wf_transition']):
                wf_tool.doActionFor(obj, entry['wf_transition'])

    do_reindex = False
    for name, roles in entry.get('local_roles', []):
        obj.manage_setLocalRoles(name, roles)
        do_reindex = True

    if entry.get('disable_acquired_local_roles', False):
        sharing_view = getMultiAdapter((obj, obj.REQUEST),
                                       name='sharing')
        sharing_view.update_inherit(False)
        do_reindex = True

    if do_reindex:
        obj.reindexObjectSecurity()

    if entry.get('disable_portlets', False):
        portletManager = getUtility(IPortletManager, name='plone.rightcolumn')
        assignable = getMultiAdapter((obj, portletManager),
                                     ILocalPortletAssignmentManager)
        assignable.setBlacklistStatus('context', True)

        portletManager = getUtility(IPortletManager, name='plone.leftcolumn')
        assignable = getMultiAdapter((obj, portletManager),
                                     ILocalPortletAssignmentManager)
        assignable.setBlacklistStatus('context', True)

    obj.reindexObject()
    return obj
