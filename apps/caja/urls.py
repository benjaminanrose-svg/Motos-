from django.urls import path
from . import views

app_name = 'caja'

urlpatterns = [
    path('', views.CajaDashboardView.as_view(), name='dashboard'),
    path('abrir/', views.abrir_caja, name='abrir'),
    path('<int:pk>/', views.CajaSesionDetailView.as_view(), name='sesion'),
    path('<int:pk>/cerrar/', views.cerrar_caja, name='cerrar'),
    path('<int:pk>/movimiento/', views.agregar_movimiento, name='movimiento'),
]
