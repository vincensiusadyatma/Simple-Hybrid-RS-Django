from django.urls import path
from . import views

urlpatterns = [
    path("", views.content_based_by_name, name="index"),
]