"""
URL configuration for back_end project.

Examples:

"""
from django.contrib import admin
from django.urls import path, include
from . import settings
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
    path('', TemplateView.as_view(template_name='index.html')),
]

if not settings.TESTING:
    urlpatterns = [
        *urlpatterns,
        path("__debug__/", include("debug_toolbar.urls")),
    ]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
