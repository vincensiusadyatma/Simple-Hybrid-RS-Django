from django.urls import path
from .views import delete_user_by_name, add_user_by_get

urlpatterns = [
    path('add-user/', add_user_by_get),
    path('delete-user/', delete_user_by_name),
]
