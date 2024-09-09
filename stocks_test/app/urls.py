from django.urls import path
from app import views

urlpatterns = [
    path("", views.home, name='home'),
    path("ticker/", views.send_chart_data, name='POST-switch-ticker'),
]