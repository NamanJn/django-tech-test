from growthstreet import models
from django import forms
from django.contrib.auth.models import User

class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = models.LoanRequest
        exclude = ["user"]

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = models.UserDetails
        exclude = ["user"]

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email"]

