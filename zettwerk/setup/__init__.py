from dependencies import install_dependencies
install_dependencies   # make pyflake happy

from catalog import handle_catalog_indexe
handle_catalog_indexe

from cleanup import cleanup_default_plone
cleanup_default_plone

from pas import set_pas_session_cookie_name, set_pas_session_cookie_timeout
set_pas_session_cookie_name
set_pas_session_cookie_timeout

from structure import handle_structure
handle_structure
