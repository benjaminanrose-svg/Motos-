from django.urls import path
from .views import ConfiguracionView

app_name = 'configuracion'

urlpatterns = [
    path('', ConfiguracionView.as_view(), name='editar'),
]
