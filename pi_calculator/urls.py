from django.urls import path
from .views import CalculatePiView, CheckProgressView

urlpatterns = [
    path('calculate_pi/', CalculatePiView.as_view(), name='calculate_pi_view'),
    path('check_progress/', CheckProgressView.as_view(), name='check_progress_view')
]
