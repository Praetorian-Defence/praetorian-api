from http import HTTPStatus

from django.utils.translation import gettext as _

from apps.api.errors import ApiException


arguments = lambda decorator: lambda *args, **kwargs: lambda func: decorator(func, *args, **kwargs)


@arguments
def permission_required(function, perm):
    def _function(request, *args, **kwargs):
        if request.user.has_perm(perm):
            return function(request, *args, **kwargs)
        else:
            raise ApiException(request, _('Permission denied.'), status_code=HTTPStatus.FORBIDDEN)
    return _function
