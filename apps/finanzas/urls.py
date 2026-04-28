from django.urls import path
from .views import FinanzasDashboardView

app_name = 'finanzas'

urlpatterns = [
    path('', FinanzasDashboardView.as_view(), name='dashboard'),
]
