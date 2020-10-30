from functools import wraps
from http import HTTPStatus

from django.utils.translation import gettext as _

from apps.api.errors import ApiException


def token_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not hasattr(request, 'user') or not request.user or not request.user.is_authenticated:
            raise ApiException(request, _("Invalid or missing credentials"), status_code=HTTPStatus.UNAUTHORIZED)
        elif request.user.is_2fa and not request.token.active_2fa:
            raise ApiException(request, _("Invalid or missing credentials"), status_code=HTTPStatus.UNAUTHORIZED)

        return func(request, *args, **kwargs)

    return inner


def superuser_required(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        if not request.user.is_authenticated or not request.user.is_superuser:
            raise ApiException(request, _('User is unauthorized.'), status_code=HTTPStatus.FORBIDDEN)

        return func(request, *args, **kwargs)

    return inner


def signature_exempt(view_func):
    """Mark a view function as being exempt from signature and apikey check."""
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.signature_exempt = True
    return wraps(view_func)(wrapped_view)
