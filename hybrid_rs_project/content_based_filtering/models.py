from django.db import models
from core.models import User, Hotel
# Create your models here.
class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    added_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'hotel')  # Supaya tidak duplikat favorit
        db_table = 'user_favorites'          # Optional: nama tabel custom

    def __str__(self):
        return f"{self.user.full_name} ❤️ {self.hotel.hotel_name}"