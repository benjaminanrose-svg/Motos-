from django.urls import path
from .views import LandingView

app_name = 'publico'

urlpatterns = [
    path('', LandingView.as_view(), name='landing'),
]
