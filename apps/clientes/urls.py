from django.urls import path
from . import views

app_name = 'clientes'

urlpatterns = [
    path('', views.ClienteListView.as_view(), name='lista'),
    path('nuevo/', views.ClienteCreateView.as_view(), name='crear'),
    path('<int:pk>/editar/', views.ClienteUpdateView.as_view(), name='editar'),
    path('<int:pk>/', views.ClienteDetailView.as_view(), name='detalle'),
]
