from django.contrib import admin
from django.urls import path, include

from django.conf import settings
from django.conf.urls.static import static

# api docs
from .aysg import urlpatterns as api_doc_urls

urlpatterns = [
    path('', admin.site.urls),
    path('api/', include('teachers.urls')),
]

if settings.DEBUG is True:
    urlpatterns += [
        path('api-auth/', include('rest_framework.urls')),
    ]
    urlpatterns += static(
        settings.MEDIA_URL,
        document_root=settings.MEDIA_ROOT
    )
    urlpatterns += api_doc_urls
