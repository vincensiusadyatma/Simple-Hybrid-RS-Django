from django.shortcuts import render

from django.http import JsonResponse
from core.models import User
from core.models import Hotel
def delete_user_by_name(request):
    full_name = request.GET.get('full_name')

    if not full_name:
        return JsonResponse({'message': 'Parameter "full_name" wajib diisi'}, status=400)

    try:
        user = User.objects.get(full_name__iexact=full_name)
        user.delete()
        return JsonResponse({'message': f'User "{full_name}" berhasil dihapus'}, status=200)
    except User.DoesNotExist:
        return JsonResponse({'message': f'User dengan nama "{full_name}" tidak ditemukan'}, status=404)



def add_user_by_get(request):
    full_name = request.GET.get('full_name')
    email = request.GET.get('email')

    if not full_name or not email:
        return JsonResponse({'message': 'Parameter "full_name" dan "email" wajib diisi'}, status=400)

    # Cek apakah email sudah terdaftar
    if User.objects.filter(email=email).exists():
        return JsonResponse({'message': f'Email "{email}" sudah digunakan'}, status=409)

    # Buat user baru
    user = User.objects.create(full_name=full_name, email=email)

    return JsonResponse({
        'message': f'User "{full_name}" berhasil ditambahkan',
        'user': {
            'id': user.id,
            'full_name': user.full_name,
            'email': user.email,
            'register_date': user.register_date
        }
    }, status=201)

def get_hotel_info_by_name(request):
    hotel_name = request.GET.get('hotel_name')

    if not hotel_name:
        return JsonResponse({'message': 'Parameter "hotel_name" wajib diisi'}, status=400)

    try:
        hotel = Hotel.objects.get(hotel_name__iexact=hotel_name)
        return JsonResponse({
            'message': f'Info hotel "{hotel_name}" berhasil ditemukan',
            'hotel': {
                'id': hotel.id,
                'hotel_name': hotel.hotel_name,
                'hotel_name_link': hotel.hotel_name_link,
                'review_score': hotel.review_score,
                'review_score_text': hotel.review_score_text,
                'review_score_title': hotel.review_score_title,
                'hotel_image': hotel.hotel_image,
                'hotel_price': float(hotel.hotel_price),
            }
        }, status=200)
    except Hotel.DoesNotExist:
        return JsonResponse({'message': f'Hotel dengan nama "{hotel_name}" tidak ditemukan'}, status=404)
    
def get_hotel_info_by_id(request, id):
    try:
        hotel = Hotel.objects.get(id=id)
        return JsonResponse({
            'message': f'Info hotel dengan ID {id} berhasil ditemukan',
            'hotel': {
                'id': hotel.id,
                'hotel_name': hotel.hotel_name,
                'hotel_name_link': hotel.hotel_name_link,
                'review_score': hotel.review_score,
                'review_score_text': hotel.review_score_text,
                'review_score_title': hotel.review_score_title,
                'hotel_image': hotel.hotel_image,
                'hotel_price': float(hotel.hotel_price),
            }
        }, status=200)
    except Hotel.DoesNotExist:
        return JsonResponse({'message': 'Hotel tidak ditemukan'}, status=404)
    
def get_all_hotels(request):
    hotels = Hotel.objects.all()
    
    hotel_list = []
    for hotel in hotels:
        hotel_list.append({
            'id': hotel.id,
            'hotel_name': hotel.hotel_name,
            'hotel_name_link': hotel.hotel_name_link,
            'review_score': hotel.review_score,
            'review_score_text': hotel.review_score_text,
            'review_score_title': hotel.review_score_title,
            'hotel_image': hotel.hotel_image,
            'hotel_price': float(hotel.hotel_price),
        })

    return JsonResponse({
        'message': f'{len(hotel_list)} hotel berhasil ditemukan',
        'hotels': hotel_list
    }, status=200)
