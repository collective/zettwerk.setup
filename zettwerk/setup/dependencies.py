# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName
from zExceptions import BadRequest
import transaction


def install_dependencies(portal, product_dependencies, product_name):
    portal_quickinstaller = getToolByName(portal, 'portal_quickinstaller')

    ## remove classic plone theme
    if portal_quickinstaller.isProductInstalled('plonetheme.classic'):
        portal_quickinstaller.uninstallProducts(['plonetheme.classic'])

    ## calling reinstall, but only the already installed ones
    ## "new" ones gets installed
    to_install = []
    to_reinstall = []
    for product in product_dependencies:
        if portal_quickinstaller.isProductInstalled(product):
            to_reinstall.append(product)
        else:
            to_install.append(product)
    if to_reinstall:
        try:
            portal_quickinstaller.reinstallProducts(to_reinstall)
        except BadRequest:
            pass  # known problem in test environment

    if to_install:
        portal_quickinstaller.installProducts(to_install)

    portal_quickinstaller.notifyInstalled(product_name)
    transaction.savepoint()
