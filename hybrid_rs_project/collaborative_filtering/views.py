import pandas as pd
from django.http import JsonResponse
from sklearn.metrics.pairwise import cosine_similarity
from core.models import Hotel, User
from collaborative_filtering.models import Favorite
from django.forms.models import model_to_dict

#fungsi collaborative
def user_based_collaborative_filtering_by_name(request):
    # Ambil nama user dan jumlah rekomendasi dari query params
    user_name = request.GET.get('user_name')
    top_n = int(request.GET.get('top_n', 3))

    # Validasi input
    if not user_name:
        return JsonResponse({'message': 'Parameter "user_name" diperlukan'}, status=400)

    # Ambil user berdasarkan nama
    try:
        user = User.objects.get(full_name__iexact=user_name)
    except User.DoesNotExist:
        return JsonResponse({'message': f'User dengan nama "{user_name}" tidak ditemukan'}, status=404)

    # Ambil semua data favorit dari database
    favorites = Favorite.objects.all().values('user_id', 'hotel_id')
    df = pd.DataFrame(favorites)

    # Cek jika data kosong
    if df.empty:
        return JsonResponse({'message': 'Data favorites kosong'}, status=404)

    # Cek apakah user memiliki data favorit
    if user.id not in df['user_id'].unique():
        return JsonResponse({'message': f'User "{user_name}" belum memfavoritkan hotel apapun'}, status=404)

    # Buat matriks user-hotel (1 jika favorit, 0 jika tidak)
    user_hotel_matrix = df.pivot_table(index='user_id', columns='hotel_id', aggfunc=lambda x: 1, fill_value=0)

    # Hitung similarity antar user
    similarity_matrix = cosine_similarity(user_hotel_matrix)
    similarity_df = pd.DataFrame(similarity_matrix, index=user_hotel_matrix.index, columns=user_hotel_matrix.index)

    # Ambil user yang paling mirip (selain dirinya sendiri)
    similar_users_series = similarity_df[user.id].drop(labels=[user.id])
    similar_users_series = similar_users_series[similar_users_series > 0].sort_values(ascending=False)

    # Cek jika tidak ada user yang mirip
    if similar_users_series.empty:
        return JsonResponse({'message': f'Tidak ada user mirip dengan "{user_name}"'}, status=404)

    # Ambil user paling mirip
    most_similar_user_id = similar_users_series.index[0]
    similarity_score = similar_users_series.iloc[0]

    try:
        most_similar_user = User.objects.get(id=most_similar_user_id)
    except User.DoesNotExist:
        return JsonResponse({'message': 'User mirip tidak ditemukan'}, status=404)

    # Ambil daftar hotel yang difavoritkan oleh user target dan user mirip
    target_user_hotels = set(user_hotel_matrix.loc[user.id][user_hotel_matrix.loc[user.id] > 0].index)
    similar_user_hotels = user_hotel_matrix.loc[most_similar_user_id]

    # Cari hotel yang hanya difavoritkan oleh user mirip
    recommended_hotel_ids = similar_user_hotels[similar_user_hotels > 0].index.difference(target_user_hotels)

    # Ambil data hotel rekomendasi dari DB
    recommended_hotels = Hotel.objects.filter(id__in=recommended_hotel_ids)[:top_n]

    # Format hasil ke bentuk JSON dengan semua property dari hotel
    recommendations = []
    for hotel in recommended_hotels:
        hotel_data = model_to_dict(hotel)
        # Jika hotel_image bukan ImageField, langsung pakai nilainya
        if hasattr(hotel, 'hotel_image') and hotel.hotel_image:
            hotel_data['hotel_image'] = hotel.hotel_image  
        recommendations.append(hotel_data)

    # Return JSON response
    return JsonResponse({
        'user_name': user.full_name,
        'similar_users': [{
            'user_id': most_similar_user.id,
            'full_name': most_similar_user.full_name,
            'similarity': round(similarity_score, 4)
        }],
        'recommendations': recommendations
    })

#fungsi tambah favorite list user
def add_favorite_by_get(request):
    # Ambil nama user dan hotel dari query params
    user_name = request.GET.get('user_name')
    hotel_name = request.GET.get('hotel_name')

    if not user_name or not hotel_name:
        return JsonResponse({'message': 'Parameter "user_name" dan "hotel_name" wajib diisi'}, status=400)

    # Cek user dan hotel
    try:
        user = User.objects.get(full_name__iexact=user_name)
        hotel = Hotel.objects.get(hotel_name__iexact=hotel_name)
    except User.DoesNotExist:
        return JsonResponse({'message': f'User dengan nama "{user_name}" tidak ditemukan'}, status=404)
    except Hotel.DoesNotExist:
        return JsonResponse({'message': f'Hotel dengan nama "{hotel_name}" tidak ditemukan'}, status=404)

    # Tambah favorite jika belum ada
    favorite, created = Favorite.objects.get_or_create(user=user, hotel=hotel)

    if created:
        return JsonResponse({'message': f'Favorite berhasil ditambahkan: {user.full_name} => {hotel.hotel_name}'})
    else:
        return JsonResponse({'message': f'Favorite sudah ada: {user.full_name} => {hotel.hotel_name}'})


#fungsi delete favorite list user
def delete_favorite_by_get(request):
    user_name = request.GET.get('user_name')
    hotel_name = request.GET.get('hotel_name')

    if not user_name or not hotel_name:
        return JsonResponse({'message': 'Parameter "user_name" dan "hotel_name" wajib diisi'}, status=400)

    # Cek user dan hotel
    try:
        user = User.objects.get(full_name__iexact=user_name)
    except User.DoesNotExist:
        return JsonResponse({'message': f'User dengan nama "{user_name}" tidak ditemukan'}, status=404)

    try:
        hotel = Hotel.objects.get(hotel_name__iexact=hotel_name)
    except Hotel.DoesNotExist:
        return JsonResponse({'message': f'Hotel dengan nama "{hotel_name}" tidak ditemukan'}, status=404)

    # Coba hapus favorite jika ada
    try:
        favorite = Favorite.objects.get(user=user, hotel=hotel)
        favorite.delete()
        return JsonResponse({'message': f'Favorite berhasil dihapus: {user.full_name} => {hotel.hotel_name}'}, status=200)
    except Favorite.DoesNotExist:
        return JsonResponse({'message': f'Favorite tidak ditemukan untuk user "{user_name}" dan hotel "{hotel_name}"'}, status=404)

    
#fungsi list favorite user
def list_favorites_by_user(request):
    user_name = request.GET.get('user_name')
    if not user_name:
        return JsonResponse({'message': 'Parameter "user_name" wajib diisi'}, status=400)

    # Cek user
    try:
        user = User.objects.get(full_name__iexact=user_name)
    except User.DoesNotExist:
        return JsonResponse({'message': f'User "{user_name}" tidak ditemukan'}, status=404)

    # Ambil data favorite hotel user
    favorites = Favorite.objects.filter(user=user).select_related('hotel')
    hotel_list = []
    for fav in favorites:
        hotel = fav.hotel
        hotel_data = {
            'id': hotel.id,
            'hotel_name': hotel.hotel_name,
            'hotel_name_link': hotel.hotel_name_link,
            'review_score': hotel.review_score,
            'review_score_text': hotel.review_score_text,
            'review_score_title': hotel.review_score_title,
            'hotel_image': hotel.hotel_image,
            'hotel_price': float(hotel.hotel_price),
        }
        hotel_list.append(hotel_data)

    return JsonResponse({
        'user': user.full_name,
        'favorites': hotel_list
    })