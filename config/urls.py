from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from apps.publico.views import LandingView
from config.views import DashboardView

urlpatterns = [
    # Django admin
    path('django-admin/', admin.site.urls),

    # Autenticación
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

    # Sitio público
    path('', LandingView.as_view(), name='landing'),

    # Panel principal (dashboard)
    path('dashboard/', DashboardView.as_view(), name='dashboard'),

    # Apps internas
    path('clientes/', include('apps.clientes.urls')),
    path('boletas/', include('apps.boletas.urls')),
    path('caja/', include('apps.caja.urls')),
    path('finanzas/', include('apps.finanzas.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
