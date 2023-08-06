"""bcmr URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static
from django.views.generic import TemplateView
from django.conf.urls import url

from rest_framework import permissions

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

from bcmr.urls import urlpatterns as bcmr_urls
from bcmr import views


schema_view = get_schema_view(
   openapi.Info(
      title="Django BCMR",
      default_version='v1',
      url='',
      description="",
      contact=openapi.Contact(
        name="Support",
        url=""
    )
   ),
   public=True,
   permission_classes=(permissions.AllowAny, ),
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(bcmr_urls)),
    # path('create_token/fungible/', views.create_token),
    url(r'^api/swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    url(r'^api/redoc/$', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    url(r'api/docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
