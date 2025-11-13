import os
import sys

BASE = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(BASE, '..'))
# Ensure project root is on sys.path
sys.path.insert(0, PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'metadata.settings')
import django

django.setup()
from django.contrib.auth import get_user_model

User = get_user_model()
users = User.objects.all()
print('COUNT:', users.count())
for u in users:
    print(f"{u.pk}\t{u.username}\tis_staff={u.is_staff}\tis_superuser={u.is_superuser}")
