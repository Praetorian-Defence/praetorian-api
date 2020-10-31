from django.urls import path

from apps.api.views import project, auth, user, remote, service, device, api_key, log_entry

urlpatterns = [
    # Authentication

    path('tokens/', auth.AuthUser.as_view(), name='auth-user'),
    path('2fa/', auth.Auth2fa.as_view(), name='auth-2fa'),

    # Api standard endpoints

    path('users/', user.UserManagement.as_view(), name='user-management'),
    path('users/me/', user.UserProfile.as_view(), name='user-profile'),
    path('users/<uuid:user_id>/', user.UserDetail.as_view()),
    path('users/<uuid:user_id>/2fa/', user.User2faActivate.as_view(), name='user-2fa'),

    path('devices/', device.DeviceManagement.as_view(), name='device-management'),

    path('remotes/', remote.RemoteManagement.as_view(), name='remote-management'),

    path('services/', service.ServiceManagement.as_view(), name='service-management'),

    path('projects/', project.ProjectManagement.as_view(), name='project-management'),

    # Admin only

    path('log_entries/', log_entry.LogEntryManagement.as_view(), name='log-entry-management'),
    path('api_keys/', api_key.ApiKeyManagement.as_view(), name='api-key-management'),
]
