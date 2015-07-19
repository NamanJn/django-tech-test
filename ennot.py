
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growthstreet.settings')

import django
django.setup()

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from growthstreetApp.models import UserDetails
users = User.objects.all()

details = UserDetails.objects.all()