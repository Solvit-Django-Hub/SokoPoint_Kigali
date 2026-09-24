import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

email = 'admin@example.com'
password = 'AdminPassword123!'

if not User.objects.filter(email=email).exists():
    User.objects.create_superuser(email, password)
    print(f'Successfully created admin user: {email}')
else:
    print(f'Admin user {email} already exists.')
