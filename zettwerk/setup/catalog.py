# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName


def handle_catalog_indexe(portal, wanted):
    """Method to add our wanted indexes to the portal_catalog. Triggers reindex
    only, if there were new indexes added. """
    # Run the catalog.xml step as that may have defined new metadata
    # columns.  We could instead add <depends name="catalog"/> to
    # the registration of our import step in zcml, but doing it in
    # code makes this method usable as upgrade step as well.
    # Remove these lines when you have no catalog.xml file.
    catalog = getToolByName(portal, 'portal_catalog')
    indexes = catalog.indexes()

    indexables = []
    for name, meta_type in wanted:
        if name not in indexes:
            catalog.addIndex(name, meta_type)
            indexables.append(name)
    if len(indexables) > 0:
        catalog.manage_reindexIndex(ids=indexables)
