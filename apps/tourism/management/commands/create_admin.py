from django.core.management.base import BaseCommand
from apps.tourism.models import CustomUser
import os


class Command(BaseCommand):
    help = 'Create a superuser automatically using environment variables'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        
        if not password:
            self.stdout.write(
                self.style.WARNING('DJANGO_SUPERUSER_PASSWORD not set. Skipping superuser creation.')
            )
            return
        
        # Check if superuser already exists
        if CustomUser.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" already exists.')
            )
            return
        
        # Create superuser
        try:
            CustomUser.objects.create_superuser(
                username=username,
                email=email,
                password=password
            )
            self.stdout.write(
                self.style.SUCCESS(f'Superuser "{username}" created successfully!')
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f'Error creating superuser: {e}')
            )
