"""PytSite Authentication Log Plugin.
"""
from pytsite import events as _events, odm as _odm, admin as _admin, lang as _lang, router as _router
from . import _eh, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Resources
_lang.register_package(__name__)  # odm_auth requires this
_lang.register_package(__name__, alias='auth_log')

# ODM models
_odm.register_model('auth_log', _model.AuthLog)

# Events handlers
_events.listen('pytsite.auth.sign_in', _eh.auth_sign_in)
_events.listen('pytsite.auth.sign_out', _eh.auth_sign_out)
_events.listen('pytsite.auth.sign_in_error', _eh.auth_sign_in_error)

# Admin sidebar menu item
admin_href = _router.ep_path('pytsite.odm_ui@browse', {'model': 'auth_log'})
_admin.sidebar.add_menu('auth', 'auth_log', 'auth_log@log', admin_href, 'fa fa-history', weight=30,
                        permissions='pytsite.odm_perm.delete.auth_log')
