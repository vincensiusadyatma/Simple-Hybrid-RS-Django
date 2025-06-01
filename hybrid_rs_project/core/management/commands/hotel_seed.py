import pandas as pd
from django.core.management.base import BaseCommand
from core.models import Hotel
from price_parser import Price

class Command(BaseCommand):
    help = 'Seed database with hotel data using pandas'

    def handle(self, *args, **kwargs):
        try:
            df = pd.read_csv('../dataset/Hotels-Jakarta.csv')
            for _, row in df.iterrows():
                parsed_price = Price.fromstring(str(row['hotel_price']))
                hotel_price = parsed_price.amount or 0.0

                Hotel.objects.create(
                    hotel_name=row['hotel_name'],
                    hotel_name_link=row['hotel_name_link'],
                    review_score=row['review_score'],
                    review_score_text=row['review_score_text'],
                    review_score_title=row['review_score_title'],
                    hotel_image=row['hotel_image'],
                    hotel_price=hotel_price
                )
            self.stdout.write(self.style.SUCCESS(f"Berhasil menyimpan {len(df)} hotel ke database."))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Gagal: {str(e)}"))
