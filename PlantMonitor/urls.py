from django.contrib import admin
from django.urls import path, include
from moisture_monitor import views  # Import views from moisture_monitor

urlpatterns = [
    path("admin/", admin.site.urls),
    path("moisture/", include("moisture_monitor.urls")),  # Include URLs from moisture_monitor app
    path("", views.view_moisture, name="moisture_view"),  # Route for the landing page
]


