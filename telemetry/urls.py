from django.urls import path
from . import views

urlpatterns = [
    path('telemetry/', views.telemetry_list),
]