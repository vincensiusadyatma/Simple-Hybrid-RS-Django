from django.shortcuts import render

from django.http import JsonResponse
from core.models import User

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