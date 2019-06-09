"""PytSite Authentication Log Plugin ODM Models
"""
__author__ = 'Oleksandr Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'

from typing import List
from pytsite import lang
from plugins import auth, odm, auth_storage_odm, geo_ip, odm_ui
from plugins.odm_auth import PERM_DELETE
from . import _api


class AuthLog(odm_ui.model.UIEntity):
    def _setup_fields(self):
        """Hook.
        """
        self.define_field(auth_storage_odm.field.User('user'))
        self.define_field(odm.field.String('ip', is_required=True))
        self.define_field(odm.field.Integer('severity', default=_api.SEVERITY_INFO))
        self.define_field(odm.field.String('description'))
        self.define_field(odm.field.Virtual('geo_ip'))

    def _setup_indexes(self):
        """Hook.
        """
        self.define_index([('user', odm.I_ASC)])
        self.define_index([('ip', odm.I_ASC)])
        self.define_index([('severity', odm.I_ASC)])

    @classmethod
    def odm_auth_permissions_group(cls) -> str:
        return 'security'

    def odm_auth_permissions(self) -> List[str]:
        return [PERM_DELETE]

    @property
    def user(self) -> auth.model.AbstractUser:
        return self.f_get('user')

    @property
    def ip(self) -> str:
        return self.f_get('ip')

    @property
    def description(self) -> str:
        return self.f_get('description')

    @property
    def severity(self) -> int:
        return self.f_get('severity')

    @property
    def geo_ip(self) -> geo_ip.GeoIP:
        return geo_ip.resolve(self.ip)

    def odm_ui_browser_setup(self, browser: odm_ui.Browser):
        """Setup ODM UI browser hook.
        """
        browser.default_sort_field = '_created'
        browser.default_sort_order = 'desc'
        browser.data_fields = [
            ('user', 'auth_log@user'),
            ('ip', 'auth_log@ip'),
            ('geo_data', 'auth_log@geo_data', False),
            ('description', 'auth_log@description', False),
            ('severity', 'auth_log@severity'),
            ('_created', 'auth_log@created'),
        ]

    def odm_ui_browser_row(self) -> dict:
        """Get single UI browser row hook.
        """
        user = ''
        try:
            if self.user:
                user = self.user.first_last_name

        except auth.error.UserNotFound:
            pass

        ip = self.ip
        g_ip = self.geo_ip
        geo = '{}, {}'.format(g_ip.country, g_ip.city) if g_ip.country else ''
        description = self.description
        modified = self.f_get('_modified', fmt='pretty_date_time')

        severity_class = 'info'
        severity_name = lang.t('auth_log@severity_info')
        if self.severity == _api.SEVERITY_WARNING:
            severity_class = 'warning'
            severity_name = lang.t('auth_log@severity_warning')
        elif self.severity == _api.SEVERITY_ERROR:
            severity_class = 'warning'
            severity_name = lang.t('auth_log@severity_error')

        severity = '<span class="label label-{}">{}</span>'.format(severity_class, severity_name)

        return {
            'user': user,
            'ip': ip,
            'geo_data': geo,
            'description': description,
            'severity': severity,
            '_created': modified,
        }
