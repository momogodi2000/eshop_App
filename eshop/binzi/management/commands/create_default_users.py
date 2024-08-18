from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = 'Create default users with specific roles'

    def handle(self, *args, **kwargs):
        users = [
            {'username': 'admin', 'password': 'admin123', 'email': 'admin@gmail.com', 'role': 'admin', 'is_superuser': True, 'is_staff': True},
            {'username': 'deliver', 'password': 'del123', 'email': 'deliver@gmail.com', 'role': 'deliver'},
        ]

        for user_data in users:
            # Pop 'role' from user_data as it's not a field in the User model.
            role = user_data.pop('role')
            
            # Check if the user already exists
            if not User.objects.filter(username=user_data['username']).exists():
                # If the user is the admin, create a superuser
                if user_data['username'] == 'admin':
                    User.objects.create_superuser(**user_data)
                    self.stdout.write(self.style.SUCCESS(f"Superuser '{user_data['username']}' created successfully"))
                else:
                    User.objects.create_user(**user_data)
                    self.stdout.write(self.style.SUCCESS(f"User '{user_data['username']}' created successfully"))
