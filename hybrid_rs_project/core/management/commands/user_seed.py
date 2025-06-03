from django.core.management.base import BaseCommand
from core.models import User
from faker import Faker
import random

class Command(BaseCommand):
    help = 'Seed the database with sample users'

    def handle(self, *args, **kwargs):
        fake = Faker()
        total = 10  

        for _ in range(total):
            full_name = fake.name()
            email = fake.unique.email()

            User.objects.create(
                full_name=full_name,
                email=email
            )

        self.stdout.write(self.style.SUCCESS(f'Successfully created {total} users'))
