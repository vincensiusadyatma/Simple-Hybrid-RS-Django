# mysite/views.py
from django.http import JsonResponse

def api_root(request):
    return JsonResponse({
        'message': 'Berhasil terkoneksi ke API',
        'status': 'ok',
        'endpoints': [
            '/core/',
            '/ratingBased/',
            '/contentBased/',
            '/collaborativeBased/',
           
        ]
    })
