"""PytSite Authentication Log Plugin Events Handlers
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from pytsite import router, lang
from plugins import auth, odm
from . import _api


def auth_sign_in(user: auth.model.AbstractUser):
    """auth.sign_in.
    """
    _create_odm_entity(user, lang.t('auth_log@login'))


def auth_sign_out(user: auth.model.AbstractUser):
    """auth.sign_out.
    """
    _create_odm_entity(user, lang.t('auth_log@logout'))


def auth_sign_in_error(exception, user: auth.model.AbstractUser):
    """auth.sign_in_error.
    """
    _create_odm_entity(user, str(exception), _api.SEVERITY_WARNING)


def _create_odm_entity(user: auth.model.AbstractUser, description: str, severity=_api.SEVERITY_INFO):
    """Helper function.
    """
    try:
        auth.switch_user_to_system()
        e = odm.dispense('auth_log')
        e.f_set('user', user)
        e.f_set('ip', router.request().real_remote_addr)
        e.f_set('severity', severity)
        e.f_set('description', description)
        e.save()
    finally:
        auth.restore_user()

    return e
