from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class LoanRequest(models.Model):
    reason = models.CharField("Reason to borrow", max_length=300)
    amount = models.PositiveIntegerField("Amount to borrow",null=False)
    loanTime = models.PositiveIntegerField("Borrow length time")
    user = models.ForeignKey(User, null=False)

    def __str__(self):
        return "User: %s | Amount: %s " % (self.user, self.amount)

    def __unicode__(self):
        return "User: %s | Amount: %s " % (self.user, self.amount)


class UserDetails(models.Model):
    userEmail = models.EmailField("Email Address", max_length=300)
    userTelephone = models.PositiveIntegerField("Contact Number", null=False)
    companyNumber = models.PositiveIntegerField("companyNumber", null=False)
    businessName = models.CharField("Business Name", max_length=100)
    businessAddress = models.CharField("Business Address", max_length=300)

    choices = (('Retail', 'Retail'),
               ('Professional', 'Professional Services'),
               ("Food", "Food & Drink"),
               ("Entertainment", "Entertainment"))

    businessSector = models.CharField(verbose_name="Business Sector", max_length=100,
                                    choices=choices, default='boolean', null=True)

    user = models.ForeignKey(User, null=False)

    def __str__(self):
        return "User: %s | Email: %s " % ( self.user, self.userEmail)

    def __unicode__(self):
        return self.__str__()

