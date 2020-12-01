from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

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
        try:
            language = Language.objects.get(code='sk')
        except Language.DoesNotExist:
            raise Exception(_('Language with code "sk" not found.'))

        kwargs.setdefault('is_superuser', True)
        kwargs.setdefault('name', name)
        kwargs.setdefault('surname', surname)
        kwargs.setdefault('language_id', language.id)
        kwargs.setdefault('is_active', True)

        password = kwargs.get('password')
        del kwargs['password']

        if kwargs.get('email'):
            kwargs['email'] = self.normalize_email(kwargs['email'])
            kwargs['username'] = self.normalize_email(kwargs['email'])

        user = self.model(**kwargs)
        user.set_password(password)
        user.save()

        return user
