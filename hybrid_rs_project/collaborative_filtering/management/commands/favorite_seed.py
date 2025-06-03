from django.core.management.base import BaseCommand
from core.models import User, Hotel
from collaborative_filtering.models import Favorite

class Command(BaseCommand):
    help = 'Seed favorite data manually with many user-hotel relationships'

    def handle(self, *args, **kwargs):
        users = User.objects.all()
        hotels = Hotel.objects.all()

        if users.count() < 5 or hotels.count() < 10:
            self.stdout.write(self.style.ERROR("Minimal 5 users dan 10 hotels dibutuhkan."))
            return

        # Manual relasi user-hotel favorit
        favorites_data = [
            # User 0
            (users[0], hotels[0]),
            (users[0], hotels[1]),
            (users[0], hotels[2]),
            (users[0], hotels[3]),

            # User 1
            (users[1], hotels[1]),
            (users[1], hotels[2]),
            (users[1], hotels[4]),
            (users[1], hotels[5]),

            # User 2
            (users[2], hotels[0]),
            (users[2], hotels[4]),
            (users[2], hotels[5]),
            (users[2], hotels[6]),

            # User 3
            (users[3], hotels[2]),
            (users[3], hotels[3]),
            (users[3], hotels[6]),
            (users[3], hotels[7]),

            # User 4
            (users[4], hotels[5]),
            (users[4], hotels[6]),
            (users[4], hotels[7]),
            (users[4], hotels[8]),

            # User 5
            (users[5], hotels[0]),
            (users[5], hotels[1]),
            (users[5], hotels[8]),
            (users[5], hotels[9]),

            # User 6
            (users[6], hotels[1]),
            (users[6], hotels[3]),
            (users[6], hotels[5]),
            (users[6], hotels[9]),

            # User 7
            (users[7], hotels[2]),
            (users[7], hotels[4]),
            (users[7], hotels[6]),
            (users[7], hotels[8]),
        ]

        created_count = 0
        for user, hotel in favorites_data:
            fav, created = Favorite.objects.get_or_create(user=user, hotel=hotel)
            if created:
                self.stdout.write(self.style.SUCCESS(f"Favorite created: {user.full_name} => {hotel.hotel_name}"))
                created_count += 1
            else:
                self.stdout.write(f"Favorite already exists: {user.full_name} => {hotel.hotel_name}")

        self.stdout.write(self.style.SUCCESS(f"\nTotal favorites created: {created_count}"))
