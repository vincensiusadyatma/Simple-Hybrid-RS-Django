from django.db import models

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    register_date = models.DateTimeField(auto_now_add=True)

class Hotel(models.Model):
    hotel_name = models.CharField(max_length=255)
    hotel_name_link = models.URLField()
    review_score = models.FloatField()
    review_score_text = models.CharField(max_length=100)
    review_score_title = models.CharField(max_length=100)
    hotel_image = models.URLField()
    hotel_price = models.DecimalField(max_digits=10, decimal_places=2)