"""Маршруты мероприятий."""

from django.urls import path

from . import views

app_name = "events"

urlpatterns = [
    path("", views.events, name="list"),
    path("available/", views.events_available, name="available"),
    path("<int:event_id>/", views.event_detail, name="detail"),
]
