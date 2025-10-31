from django.core.management.base import BaseCommand
from create_test_data import create_test_data

class Command(BaseCommand):
    help = 'Create test data for authentication system'

    def handle(self, *args, **options):
        create_test_data()
        self.stdout.write(
            self.style.SUCCESS('Successfully created test data')
        )