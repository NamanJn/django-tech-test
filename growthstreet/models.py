from django.core.exceptions import ValidationError
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


from django.core.validators import MaxValueValidator, MinValueValidator



def RegistrationNumberValidator(value):
    if len(str(value))  != 8:
        raise ValidationError('Registration has to be an 8-digit number.')

class LoanRequest(models.Model):
    reason = models.CharField("Reason to borrow", max_length=300)
    amount = models.PositiveIntegerField(u"Amount (\u00A3)", null=False,
                                         validators=[MinValueValidator(10000), MaxValueValidator(100000)])
    loanTime = models.PositiveIntegerField("Borrow time (days)")
    user = models.ForeignKey(User, null=False)

    def __str__(self):
        return "User: %s | Amount: %s | Time: %s days." % (self.user, self.amount, self.loanTime)

    def __unicode__(self):
        return self.__str__()



class UserDetails(models.Model):

    userTelephone = models.PositiveIntegerField("Contact Number", null=False)
    companyNumber = models.PositiveIntegerField("Company Number", null=False,
                                                validators=[RegistrationNumberValidator])
    businessName = models.CharField("Business Name", max_length=100)
    businessAddress = models.CharField("Business Address", max_length=300)

    choices = (('Retail', 'Retail'),
               ('Professional', 'Professional Services'),
               ("Food", "Food & Drink"),
               ("Entertainment", "Entertainment"))

    businessSector = models.CharField(verbose_name="Business Sector", max_length=100,
                                    choices=choices, default='Food', null=True)

    user = models.OneToOneField(User, null=False)

    def __str__(self):
        return "User: %s | Contact: %s " % (self.user, self.userTelephone)

    def __unicode__(self):
        return self.__str__()


