from django.urls import path
from . import views

urlpatterns = [
    path("", views.view_moisture, name="view_moisture"),
    path("latest/", views.latest_reading, name="latest_reading"),  # Define the latest reading URL
]
