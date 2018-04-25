"""PytSite Authentication Log Plugin Events Handlers
"""
__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router as _router, lang as _lang
from plugins import auth as _auth, odm as _odm
from . import _api


def auth_sign_in(user: _auth.model.AbstractUser):
    """auth.sign_in.
    """
    _create_odm_entity(user, _lang.t('auth_log@login'))


def auth_sign_out(user: _auth.model.AbstractUser):
    """auth.sign_out.
    """
    _create_odm_entity(user, _lang.t('auth_log@logout'))


def auth_sign_in_error(exception, user: _auth.model.AbstractUser):
    """auth.sign_in_error.
    """
    _create_odm_entity(user, str(exception), _api.SEVERITY_WARNING)


def _create_odm_entity(user: _auth.model.AbstractUser, description: str, severity=_api.SEVERITY_INFO):
    """Helper function.
    """
    try:
        _auth.switch_user_to_system()
        e = _odm.dispense('auth_log')
        e.f_set('user', user)
        e.f_set('ip', _router.request().remote_addr)
        e.f_set('severity', severity)
        e.f_set('description', description)
        e.save()
    finally:
        _auth.restore_user()

    return e
