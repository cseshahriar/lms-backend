from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from django.urls import include, re_path

schema_view = get_schema_view(
    openapi.Info(
        title="LMS API",
        default_version='v1',
        description="Learning Management API",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="cse.shahriar.hosen@gmail.com"),
        license=openapi.License(name="Private License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    re_path(
        r'^swagger(?P<format>\.json|\.yaml)$',
        schema_view.without_ui(cache_timeout=0), name='schema-json'
    ),
    re_path(
        r'^swagger/$',
        schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'  # noqa
    ),
    re_path(
        '', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'
    ),
]