from django.core.management.base import BaseCommand
from django.core.management import call_command

class Command(BaseCommand):
    help = 'Jalankan semua seeder dari setiap app'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("🟡 Menjalankan semua seed..."))

        try:
            call_command('user_seed')
            call_command('hotel_seed')
            call_command('favorite_seed')
           
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"❌ Gagal menjalankan seeder: {e}"))
            return

        self.stdout.write(self.style.SUCCESS("✅ Semua seeder berhasil dijalankan."))
