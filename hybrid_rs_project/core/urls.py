from django.urls import path
from .views import delete_user_by_name, add_user_by_get,get_hotel_info_by_name, get_hotel_info_by_id, get_all_hotels

urlpatterns = [
    path('add-user/', add_user_by_get),
    path('delete-user/', delete_user_by_name),
    path('hotels/', get_all_hotels),
    path('hotel-info/<int:id>/', get_hotel_info_by_id),

]
