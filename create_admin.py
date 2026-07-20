import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
django.setup()

from django.contrib.auth.models import User

username = "admin"
password = "Admin@123"
email = "admin@example.com"

user, created = User.objects.get_or_create(
    username=username,
    defaults={"email": email},
)

user.email = email
user.is_staff = True
user.is_superuser = True
user.set_password(password)
user.save()

print("Admin user is ready.")