from django.contrib import admin
from django.urls import path, include
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/teachers/', include('teachers.urls')),
]

if settings.DEBUG is True:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),
        # browsable API login
    ]
