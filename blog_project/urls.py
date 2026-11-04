"""Configuración de URLs del proyecto Blog Django."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from posts import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("posts.urls")),
    path("accounts/register/", views.RegisterView.as_view(), name="register"),
    path("accounts/login/", views.CustomLoginView.as_view(), name="login"),
    path("accounts/logout/", views.CustomLogoutView.as_view(), name="logout"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
