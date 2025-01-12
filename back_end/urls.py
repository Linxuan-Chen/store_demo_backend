"""
URL configuration for back_end project.

Examples:

"""
from django.contrib import admin
from django.conf import settings
from django.urls import path, include
from .settings import common, dev, prod
from django.views.generic import TemplateView
from django.conf.urls.static import static


api_urlpatterns = [
    path('store/', include('store.urls'))
]

urlpatterns = [
    path('api/', include(api_urlpatterns)),
    path('admin/', admin.site.urls),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('account/', include('account.urls')),
]

if not common.TESTING:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    ]
if settings.DEBUG:
    urlpatterns += static(dev.MEDIA_URL,
                          document_root=dev.MEDIA_ROOT)
    urlpatterns += [path('silk/', include('silk.urls', namespace='silk'))]
