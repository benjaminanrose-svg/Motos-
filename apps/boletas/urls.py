from django.urls import path
from . import views

app_name = 'boletas'

urlpatterns = [
    path('', views.BoletaListView.as_view(), name='lista'),
    path('nueva/', views.BoletaCreateView.as_view(), name='crear'),
    path('<int:pk>/', views.BoletaDetailView.as_view(), name='detalle'),
    path('<int:pk>/editar/', views.BoletaUpdateView.as_view(), name='editar'),
    path('<int:pk>/pagar/', views.boleta_pagar, name='pagar'),
    path('<int:pk>/anular/', views.boleta_anular, name='anular'),
    path('<int:pk>/pdf/', views.boleta_pdf, name='pdf'),
    path('exportar/csv/', views.boletas_csv, name='csv'),
]
