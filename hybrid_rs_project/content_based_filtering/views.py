import pandas as pd
from django.http import JsonResponse
from sklearn.preprocessing import StandardScaler
from sklearn.metrics.pairwise import cosine_similarity
from core.models import Hotel  

def content_based_by_name(request):
    hotel_name_query = request.GET.get('hotel_name')
    top_n = int(request.GET.get('top_n', 3))

    queryset = Hotel.objects.all().values(
        'id', 'hotel_name', 'review_score', 'review_score_text', 'review_score_title', 'hotel_price'
    )
    df = pd.DataFrame(list(queryset))

    if df.empty:
        return JsonResponse({'message': 'Data hotel kosong'}, status=404)

    # Preprocessing review_score_text dan hotel_price
    df['review_score_text'] = (
        df['review_score_text']
        .str.replace(',', '', regex=False)
        .str.replace(' reviews', '', regex=False)
        .astype(int)
    )

    df['hotel_price'] = (
        df['hotel_price']
        .astype(str)
        .str.replace('Rp', '', regex=False)
        .str.replace('.', '', regex=False)
        .str.replace(',', '', regex=False)
        .astype(int)
    )

    # One-hot encode :v biar jadi kategori number
    df = pd.get_dummies(df, columns=['review_score_title'])

    # Fitur yang dipakai
    features = ['review_score_text', 'hotel_price'] + \
        [col for col in df.columns if col.startswith('review_score_title_')]

    # Normalisasi dan hitung cosine similarity :V
    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(df[features])
    similarity_matrix = cosine_similarity(scaled_features)

    # Cari index hotel target
    try:
        hotel_index = df[df['hotel_name'].str.lower() == hotel_name_query.lower()].index[0]
    except IndexError:
        return JsonResponse({'message': f'Hotel "{hotel_name_query}" tidak ditemukan'}, status=404)

    similarity_scores = list(enumerate(similarity_matrix[hotel_index]))
    similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)

    # Ambil hotel mirip selain dirinya sendiri
    similar_indices = similarity_scores[1:top_n + 1]

    recommendations = []
    for i, score in similar_indices:
        hotel = df.iloc[i]
        recommendations.append({
        'hotel_name': hotel['hotel_name'],
        'review_score': float(hotel['review_score']),
        'hotel_price': int(hotel['hotel_price']),
        'cosine_similarity': round(float(score), 4)
        })


    return JsonResponse({
        'target_hotel': df.iloc[hotel_index]['hotel_name'],
        'recommendations': recommendations
    })
