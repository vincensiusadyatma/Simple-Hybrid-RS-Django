from django.shortcuts import render
from django.http import JsonResponse
# Create your views here.
from django.http import HttpResponse
from core.models import Hotel
import pandas as pd

def index(request):
   hotels = Hotel.objects.all().values()
   hotels = Hotel.objects.all().order_by('-review_score').values()  # ubah menjadi QuerySet of dict
   df = pd.DataFrame(list(hotels)).head(50)

   #return HttpResponse(df.to_html())
   return JsonResponse(df.to_dict(orient='records'), safe=False)