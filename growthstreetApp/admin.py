from django.contrib import admin

# Register your models here.
from models import LoanRequest, UserDetails

admin.site.register(LoanRequest)
admin.site.register(UserDetails)
