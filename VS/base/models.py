
from datetime import date
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from elections.models import Constituency

# Create your models here.

class UserData(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)

    profile_pic=models.ImageField(null= True , blank=True , default="defaults/profile_pic.jpg" , upload_to="profile/")
    first_name=models.CharField(max_length=15,default="")
    last_name=models.CharField(max_length=15,default="")
    dob = models.DateField(default=date.today)
    father_name=models.CharField(max_length=30,default="",blank=True)
    mother_name=models.CharField(max_length=30,default="",blank=True)

    adhaar_number =models.CharField(max_length=20,default="" ,unique=True)
    mobile_number=models.CharField(max_length=10,default="")

    region= models.ForeignKey(Constituency , on_delete=models.SET_NULL,null=True)

    class RegistrationStatus(models.TextChoices):
        NOT_APPLIED = 'na', _('NotApplied')
        PENDING = 'pending', _('Pending')
        APPROVED = 'approved',_('Approved')
    
    class Authority(models.TextChoices):
        NONE = 'none', _('None')
        SUPER_ADMIN = 'super', _('SuperAdmin')
        REG_ADMIN = 'regional', _('RegionalAdmin')

    
    registration_status = models.CharField(max_length=10, choices=RegistrationStatus.choices , default= RegistrationStatus.NOT_APPLIED)
    authority = models.CharField(max_length=10, choices=Authority.choices , default=Authority.NONE)
    voter_id = models.CharField(max_length=20, default="None")


    def __str__(self) -> str:
        return self.first_name + " " + self.last_name + " data"


class Notification(models.Model):
    class Level(models.TextChoices):
        NONE = 'none', _('None')
        SUPER_ADMIN = 'broadcast', _('Brodcast')
    level =  models.CharField(max_length=10, choices=Level.choices , default=Level.NONE)
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null=True, blank=True)
    message = models.TextField(max_length=500, default="")

