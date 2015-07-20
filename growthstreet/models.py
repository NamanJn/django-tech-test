from django.core.exceptions import ValidationError
from django.forms import ValidationError
from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class LoanRequest(models.Model):
    reason = models.CharField("Reason to borrow", max_length=300)
    amount = models.PositiveIntegerField(u"Amount (\u00A3)", null=False)

    loanTime = models.PositiveIntegerField("Borrow time (days)")
    user = models.ForeignKey(User, null=False)

    def clean(self):
        super(LoanRequest, self).clean()
        if self.amount < 10000 or self.amount > 100000:
            raise ValidationError("Amount needs to be between 10000 and 100000.")

    def save(self, *args, **kwargs):

        self.clean()
        super(LoanRequest, self).save(*args, **kwargs)

    def __str__(self):
        return "User: %s | Amount: %s | Time: %s days." % (self.user, self.amount, self.loanTime)

    def __unicode__(self):
        return self.__str__()


class UserDetails(models.Model):

    userTelephone = models.PositiveIntegerField("Contact Number", null=False)
    companyNumber = models.PositiveIntegerField("Company Number", null=False)

    businessName = models.CharField("Business Name", max_length=100)
    businessAddress = models.CharField("Business Address", max_length=300)

    choices = (('Retail', 'Retail'),
               ('Professional', 'Professional Services'),
               ("Food", "Food & Drink"),
               ("Entertainment", "Entertainment"))

    businessSector = models.CharField(verbose_name="Business Sector", max_length=100,
                                    choices=choices, default='Food', null=True)

    user = models.OneToOneField(User, null=False)

    def clean(self):
        super(UserDetails, self).clean()
        if len(str(self.companyNumber)) != 8:
            raise ValidationError('Registration Number has to be an 8-digit number.')


    def save(self, *args, **kwargs):

        self.clean()
        super(UserDetails, self).save(*args, **kwargs)

    def __str__(self):
        return "User: %s | Contact: %s " % (self.user, self.userTelephone)

    def __unicode__(self):
        return self.__str__()


