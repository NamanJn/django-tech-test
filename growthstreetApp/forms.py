from growthstreetApp import models
from django import forms


class LoanRequestForm(forms.ModelForm):
    class Meta:
        model = models.LoanRequest
        exclude = ["user"]

class UserDetailsForm(forms.ModelForm):
    class Meta:
        model = models.UserDetails
        exclude = ["user"]

# class AddFormFieldFormx(forms.ModelForm):
#     class Meta:
#         model = FormField
#         exclude = ["ownedByWhichTemplate"];