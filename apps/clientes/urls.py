from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='lista'),
    path('nuevo/', views.ClienteCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='editar'),
    # Motos
    path('<int:cliente_pk>/motos/nueva/', views.MotoCreateView.as_view(), name='moto_crear'),
    path('motos/<int:pk>/editar/', views.MotoUpdateView.as_view(), name='moto_editar'),
    path('motos/<int:pk>/eliminar/', views.MotoDeleteView.as_view(), name='moto_eliminar'),
    # AJAX
    path('api/search/', views.cliente_search_ajax, name='search_ajax'),
    path('api/<int:pk>/motos/', views.cliente_motos_ajax, name='motos_ajax'),
    # CSV
    path('exportar/csv/', views.clientes_csv, name='csv'),
]
