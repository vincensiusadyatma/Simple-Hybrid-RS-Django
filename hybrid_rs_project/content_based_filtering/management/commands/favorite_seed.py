from django.core.management.base import BaseCommand
from core.models import User, Hotel
from content_based_filtering.models import Favorite
class Command(BaseCommand):
    #seeder buat simpan relasi user interaksi dengan hotel
    help = 'Seed favorite data for users and hotels'

    def handle(self, *args, **kwargs):
        users = User.objects.all()[:3]    
        hotels = Hotel.objects.all()[:5] 

        favorites_data = [
            (users[0], hotels[0]),
            (users[0], hotels[1]),
            (users[1], hotels[2]),
            (users[1], hotels[3]),
            (users[2], hotels[4]),
            (users[2], hotels[0]),
        ]

        created_count = 0
        for user, hotel in favorites_data:
            fav, created = Favorite.objects.get_or_create(user=user, hotel=hotel)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Favorite created: {user.full_name} -> {hotel.hotel_name}"))
                created_count += 1
            else:
                self.stdout.write(f"Favorite already exists: {user.full_name} -> {hotel.hotel_name}")

        self.stdout.write(self.style.SUCCESS(f"Total favorites created: {created_count}"))
