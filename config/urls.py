from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from apps.publico.views import LandingView
from config.views import DashboardView

handler404 = 'config.views.error_404'
handler500 = 'config.views.error_500'

urlpatterns = [
    path('django-admin/', admin.site.urls),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('', LandingView.as_view(), name='landing'),
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    path('clientes/', include('apps.clientes.urls')),
    path('boletas/', include('apps.boletas.urls')),
    path('caja/', include('apps.caja.urls')),
    path('finanzas/', include('apps.finanzas.urls')),
    path('configuracion/', include('apps.configuracion.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
