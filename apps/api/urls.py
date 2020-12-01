from django.urls import path

from apps.api.views import project, auth, user, remote, service, device, api_key, log_entry, temporary_user

urlpatterns = [
    # Authentication

    path('tokens/', auth.AuthUser.as_view(), name='auth-user'),
    path('2fa/', auth.Auth2fa.as_view(), name='auth-2fa'),

    # Api standard endpoints

    path('users/', user.UserManagement.as_view(), name='user-management'),
    path('users/me/', user.UserProfile.as_view(), name='user-profile'),
    path('users/<uuid:user_id>/', user.UserDetail.as_view(), name='user-detail'),
    path('users/<uuid:user_id>/2fa/', user.User2faActivate.as_view(), name='user-2fa'),

    path('temporary_users/create/', temporary_user.create_temporary_user, name='temporary-user-create'),

    path('password/recovery/<str:email>/', user.PasswordRecoveryManagement.as_view(), name='password_recovery'),
    path('password/activate/', user.PasswordActivateManagement.as_view(), name='password_activate'),

    path('devices/', device.DeviceManagement.as_view(), name='device-management'),
    path('devices/<uuid:device_id>/', device.DeviceDetail.as_view(), name='device-detail'),

    path('remotes/', remote.RemoteManagement.as_view(), name='remote-management'),
    path('remotes/<uuid:remote_id>/', remote.RemoteDetail.as_view(), name='remote-detail'),

    path('services/', service.ServiceManagement.as_view(), name='service-management'),
    path('services/<uuid:service_id>/', service.ServiceDetail.as_view(), name='service-detail'),

    path('projects/', project.ProjectManagement.as_view(), name='project-management'),
    path('projects/<uuid:project_id>/', project.ProjectDetail.as_view(), name='project-detail'),

    # Admin only

    path('log_entries/', log_entry.LogEntryManagement.as_view(), name='log-entry-management'),
    path('api_keys/', api_key.ApiKeyManagement.as_view(), name='api-key-management'),
    path('api_keys/<uuid:api_key_id>/', api_key.ApiKeyDetail.as_view(), name='api-key-detail'),
]
