"""PytSite Authentication Log Plugin
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load_wsgi():
    from pytsite import events, router
    from plugins import odm, admin
    from . import _eh, _model

    # ODM models
    odm.register_model('auth_log', _model.AuthLog)

    # Events handlers
    events.listen('auth@sign_in', _eh.auth_sign_in)
    events.listen('auth@sign_out', _eh.auth_sign_out)
    events.listen('auth@sign_in_error', _eh.auth_sign_in_error)

    # Admin's sidebar menu
    admin_href = router.rule_path('odm_ui@admin_browse', {'model': 'auth_log'})
    admin.sidebar.add_menu('security', 'auth_log', 'auth_log@log', admin_href, 'fa fas fa-history', weight=30)
