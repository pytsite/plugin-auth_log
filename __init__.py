"""PytSite Authentication Log Plugin
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


def plugin_load_uwsgi():
    from pytsite import events, lang, router
    from plugins import odm, admin
    from . import _eh, _model

    # Resources
    lang.register_package(__name__)

    # ODM models
    odm.register_model('auth_log', _model.AuthLog)

    # Events handlers
    events.listen('auth@sign_in', _eh.auth_sign_in)
    events.listen('auth@sign_out', _eh.auth_sign_out)
    events.listen('auth@sign_in_error', _eh.auth_sign_in_error)

    # Admin's sidebar section
    if not admin.sidebar.get_section('security'):
        admin.sidebar.add_section('security', 'auth_log@security', 1000)

    # Admin's sidebar menu
    admin_href = router.rule_path('odm_ui@browse', {'model': 'auth_log'})
    admin.sidebar.add_menu('security', 'auth_log', 'auth_log@log', admin_href, 'fa fa-history', weight=30,
                            permissions='odm_auth@delete.auth_log')
