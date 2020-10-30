from django.contrib.auth.base_user import BaseUserManager

from apps.core.managers.base import BaseManager
from apps.core.models.language import Language


class UserManager(BaseUserManager, BaseManager):
    use_in_migrations = True

    def get_by_natural_key(self, username):
        conditions = {
            f"{self.model.USERNAME_FIELD}__iexact": username
        }
        return self.get(**conditions)

    def create_superuser(self, name, surname, **kwargs):
        kwargs.setdefault('is_superuser', True)

        kwargs.setdefault('name', name)

        kwargs.setdefault('surname', surname)

        language = Language.objects.get(code='sk')

        kwargs.setdefault('language_id', language.id)

        kwargs.setdefault('is_active', True)

        if kwargs.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._save_user(self.model(), **kwargs)

    def _save_user(self, user, **extra_fields):
        is_new_record = user._state.adding

        if extra_fields.get('email') is not None:
            user.email = self.normalize_email(extra_fields.get('email'))
            user.username = self.normalize_email(extra_fields.get('email'))

        if extra_fields.get('username') is not None:
            user.username = extra_fields.get('username')

        if extra_fields.get('name') is not None:
            user.name = extra_fields.get('name')

        if extra_fields.get('surname') is not None:
            user.surname = extra_fields.get('surname')

        if extra_fields.get('password') is not None:
            user.set_password(extra_fields.get('password'))

        if extra_fields.get('language_id') is not None:
            user.language_id = extra_fields.get('language_id')

        if extra_fields.get('phone') is not None:
            user.phone = extra_fields.get('phone')

        if extra_fields.get('default_organisation_id') is not None:
            user.default_organisation_id = extra_fields.get('default_organisation_id')
        else:
            user.default_organisation_id = None

        user.is_active = extra_fields.get('is_active', user.is_active)
        user.name = extra_fields.get('name', None if is_new_record else user.name)
        user.surname = extra_fields.get('surname', None if is_new_record else user.surname)
        user.is_superuser = extra_fields.get('is_superuser', False)

        user.save()
        return user
