from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from growthstreet.models import LoanRequest, UserDetails


class PersonalInfo(admin.StackedInline):
    model = UserDetails
    can_delete = False
    verbose_name_plural = 'User Personal Information'


class UserAdmin(UserAdmin):
    inlines = (PersonalInfo,)


# Re-register UserAdmin
admin.site.unregister(User)
admin.site.register(User, UserAdmin)

# Register LoanRequest
admin.site.register(LoanRequest)