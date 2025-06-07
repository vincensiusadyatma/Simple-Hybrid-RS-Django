from django.urls import path
from . import views

urlpatterns = [
    path("", views.user_based_collaborative_filtering_by_name, name="index"),
    path("add-favorites", views.add_favorite_by_get, name="index"),
    path("delete-favorites", views.delete_favorite_by_get, name="index"),
    path("list-favorites", views.list_favorites_by_user, name="index"),
]