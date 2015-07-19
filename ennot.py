
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'growthstreet.settings')
import sqlite3
import django
django.setup()

from django.contrib.auth.models import User
#from django.contrib.sites.models import Site
from growthstreet.models import UserDetails,LoanRequest
users = User.objects.all()

details = UserDetails.objects.all()

conn = sqlite3.connect('db.sqlite3')
c = conn.cursor()

c.execute("select * from auth_user")
results = c.fetchall()
print results


c.execute("select * from growthstreet_userdetails")
a = c.fetchall()

# create Loan Request with less than 10,000
request = LoanRequest(reason="adf",amount=100,loanTime=2,user=users[0])
#request.clean()
#request.save()
