import re
import uuid
from datetime import datetime
from http import HTTPStatus
from typing import TypedDict, Dict, Union, List, Optional
from urllib.parse import quote

import ldap
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import gettext as _
from rolepermissions.roles import assign_role

from apps.api.errors import ActiveDirectoryManagerException
from apps.core.models import AuthSource, AuthSourceGroup, Language, UserProjectDevice, Project, Device
from apps.core.services.requestor import Requestor

User = get_user_model()

EXPIRED = 0
ENABLE = 'Enable'
EXPIRE = 'Expire'


class LdapConfig(TypedDict):
    SERVER_URI: str
    BASE_URL: str
    BIND_DN: str
    BIND_PASSWORD: str
    USER_ATTR_MAP: Dict[str, str]
    USER_SEARCH: Dict[str, str]
    GROUP_SEARCH: Dict[str, str]
    USER_LOGIN_ATTR: str
    AUTH_SOURCE_LDAP_NAME: str


class CustomLDAPBackend(ModelBackend):
    def __init__(self):
        self.ldap_auth_sources = AuthSource.objects.filter(driver=AuthSource.DriverEnum.LDAP, is_active=True)

    def _deactivate_user(self, username):
        try:
            user_to_deactivate = User.objects.get(username=username)
        except User.DoesNotExist:
            return

        if self.ldap_auth_sources.filter(pk=user_to_deactivate.auth_source.pk).exists():
            user_to_deactivate.is_active = False
            user_to_deactivate.save()

    @staticmethod
    def _ldap(
        username: str, password: str, ldap_auth_source: AuthSource, connection, attrs, config, request
    ) -> Union[User, None]:
        try:
            connection.simple_bind_s(username, password)
        except ldap.LDAPError:
            return None

        try:
            user = User.all_objects.get(username=attrs[config['USER_ATTR_MAP']['username']][0].decode())
        except User.DoesNotExist:
            user = User(username=attrs[config['USER_ATTR_MAP']['username']][0].decode(), auth_source=ldap_auth_source)
            user.set_unusable_password()
        else:
            if not user.is_active:
                user.is_active = True
                user.auth_source = ldap_auth_source

        for model_property, ldap_property in config["USER_ATTR_MAP"].items():
            if ldap_property in attrs:
                setattr(user, model_property, attrs[ldap_property][0].decode())
        user.language = Language.objects.get(code='sk')
        user.save()

        # TODO: update based on groups
        assign_role(user, 'devops')
        device, created = Device.objects.get_or_create(
            user=user,
            name=user.email,
            certificate=uuid.uuid4(),
            ip_address='127.0.0.1'
        )
        UserProjectDevice.objects.get_or_create(user=user, project=Project.objects.first(), device=device)

        return user

    def authenticate(self, request, username=None, password=None, **kwargs):
        user = None

        if not username:
            return user

        for ldap_auth_source in self.ldap_auth_sources:
            config: LdapConfig = ldap_auth_source.content
            connection = ldap.initialize(uri=config["SERVER_URI"])
            connection.set_option(ldap.OPT_REFERRALS, 0)
            try:
                connection.simple_bind_s(config['BIND_DN'], config['BIND_PASSWORD'])
            except ldap.LDAPError:
                return User

            result_id = connection.search(
                config['USER_SEARCH']['base_dn'],
                ldap.SCOPE_SUBTREE,
                config['USER_SEARCH']['filterstr'] % {'user': username}
            )
            user_type, profiles = connection.result(result_id, 0)

            if profiles[0][0]:
                name, attrs = profiles[0]

                user = self._ldap(
                    username=attrs[config['USER_LOGIN_ATTR']][0].decode(),
                    password=password,
                    ldap_auth_source=ldap_auth_source,
                    connection=connection,
                    attrs=attrs,
                    config=config,
                    request=request
                )

            if user:
                break
        else:
            try:
                self._deactivate_user(username)
            except ImproperlyConfigured:
                pass

        return user


class LDAPService:
    class User(TypedDict):
        distinguishedName: str
        mail: str
        whenCreated: datetime
        whenChanged: datetime
        pwdLastSet: Optional[datetime]
        enabled: bool
        passwordExpired: bool
        telephoneNumber: Optional[str]
        directReports: List[str]
        badPwdCount: int
        badPasswordTime: Optional[datetime]
        lastLogon: Optional[datetime]
        manager: str
        memberOf: List[str]
        givenName: str
        sn: str
        sAMAccountName: str

    def __init__(self, user: get_user_model()):
        self._user = user
        self._config: LdapConfig = user.auth_source.content
        self._requestor = Requestor(api_url=self._config['BASE_URL'])

        connection = ldap.initialize(uri=self._config["SERVER_URI"])
        connection.set_option(ldap.OPT_REFERRALS, 0)
        try:
            connection.simple_bind_s(self._config['BIND_DN'], self._config['BIND_PASSWORD'])
        except ldap.LDAPError:
            raise ActiveDirectoryManagerException(
                title=_('Could not connect to active directory!'), status=HTTPStatus.CONFLICT
            )
        self._connection = connection

    @property
    def requestor(self) -> Requestor:
        return self._requestor

    @staticmethod
    def _parse_cn_from_ldap_group(ldap_group):
        """
        Parses the CN value from an LDAP group string.
        """
        match = re.search(r'CN=([^,]+)', ldap_group)
        if match:
            return match.group(1)
        return None

    def _update_groups(self, user, groups):
        user.groups.clear()
        for ldap_group in groups:
            """
            Loop LDAP groups, extract the CN, checks if this group exists in the Django database,
            and adds the user to the group if it exists.
            """
            cn = self._parse_cn_from_ldap_group(ldap_group)

            if cn:
                try:
                    django_group = user.auth_source.groups.get(external=cn)
                except (AuthSourceGroup.DoesNotExist, AttributeError):
                    pass
                else:
                    user.groups.add(django_group.group)

    def _get_distinguished_name(self):
        distinguished_name = None

        result_id = self._connection.search(
            self._config['USER_SEARCH']['base_dn'],
            ldap.SCOPE_SUBTREE,
            self._config['USER_SEARCH']['filterstr'] % {'user': self._user.email}
        )
        user_type, profiles = self._connection.result(result_id, 0)

        if profiles[0][0]:
            name, attrs = profiles[0]

            distinguished_name = attrs['distinguishedName'][0].decode()

        if not distinguished_name:
            raise ActiveDirectoryManagerException(title='User not found!', status=HTTPStatus.NOT_FOUND)

        return distinguished_name

    def _update_user_data_and_groups(self, user, user_model):
        for model_property, ldap_property in self._config["USER_ATTR_MAP"].items():
            if ldap_property in user:
                setattr(user_model, model_property, user[ldap_property])

        self._update_groups(user_model, user['memberOf'])

    def get_user(self) -> User:
        user: LDAPService.User = self.requestor.request(
            method='GET',
            endpoint_url=settings.LDAP_USER_DETAIL_URL.format(distinguishedName=quote(self._get_distinguished_name()))
        )

        return user

    def update_user(self, data: dict, user_model: get_user_model()) -> get_user_model():
        user: LDAPService.User = self.requestor.request(
            method='PUT',
            endpoint_url=settings.LDAP_USER_DETAIL_URL.format(distinguishedName=quote(self._get_distinguished_name())),
            payload=data
        )

        self._update_user_data_and_groups(user, user_model)
        user_model.save()

        return user

    def change_password(self, data: dict) -> User:
        username = self._get_distinguished_name()
        try:
            self._connection.simple_bind_s(username, data['old_password'])
        except ldap.LDAPError as e:
            raise ActiveDirectoryManagerException(
                title=_('Invalid credentials!'), status=HTTPStatus.BAD_REQUEST, previous=e
            )

        user: LDAPService.User = self.requestor.request(
            method='PUT',
            endpoint_url=settings.LDAP_UPDATE_PASSWORD_URL.format(
                distinguishedName=quote(self._get_distinguished_name())
            ),
            payload=data
        )

        return user
