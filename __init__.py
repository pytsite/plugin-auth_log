"""PytSite Authentication Log Plugin
"""
from pytsite import events as _events, lang as _lang, router as _router
from plugins import odm as _odm, admin as _admin
from . import _eh, _model

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

# Resources
_lang.register_package(__name__)

# ODM models
_odm.register_model('auth_log', _model.AuthLog)

# Events handlers
_events.listen('auth.sign_in', _eh.auth_sign_in)
_events.listen('auth.sign_out', _eh.auth_sign_out)
_events.listen('auth.sign_in_error', _eh.auth_sign_in_error)

# Admin sidebar menu item
admin_href = _router.rule_path('odm_ui@browse', {'model': 'auth_log'})
_admin.sidebar.add_menu('auth', 'auth_log', 'auth_log@log', admin_href, 'fa fa-history', weight=30,
                        permissions='odm_auth.delete.auth_log')
