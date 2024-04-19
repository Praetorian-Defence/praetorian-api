from typing import Union

from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.core.exceptions import ValidationError
from django.utils import timezone

from apps.core.models import Token

User = get_user_model()


class TokenBackend(ModelBackend):
    def _by_token(self, token) -> Union[User, None]:
        try:
            t = Token.objects.get(pk=token)
        except (Token.DoesNotExist, ValidationError):
            return None

        t.user.last_login = timezone.now()
        t.user.save()

        return t.user

    def authenticate(self, request, **kwargs) -> Union[User, None]:
        if kwargs.get('token'):
            user = self._by_token(kwargs.get('token'))
        else:
            user = super().authenticate(request, **kwargs)

        return user
