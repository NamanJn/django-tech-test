
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growthstreet.settings')
import sqlite3
import django
django.setup()

from django.contrib.auth.models import User
from growthstreet.models import UserDetails,LoanRequest

users = User.objects.all()
usernames = [['naman','nj1411@ic.ac.uk'],
             ['jainy','namanjn07@hotmail.com'],
             ['namu','nj1411@ic.ac.uk'],
             ]

counter = 0
for i, email in usernames:
    a = User.objects.create_user(username=i, password=i, email=email)
    a.is_active = True
    if i == 'jainy': # jainy is the superuser
        a.is_staff = True
        a.is_superuser = True
    a.save()

    request = LoanRequest(reason = "broke%s" %counter , amount = 10000+counter, loanTime=1+counter, user = a)
    request.save()
    counter += 3


# database querying
conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()
c.execute("select * from auth_user")
results = c.fetchall()
print results
