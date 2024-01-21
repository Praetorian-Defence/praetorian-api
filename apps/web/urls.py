from django.urls import path

from apps.web.views import log

urlpatterns = [
    path("", log.LogView.as_view(), name='log_list'),
    path("<uuid:log_id>", log.LogDetail.as_view(), name='log_detail'),
]
