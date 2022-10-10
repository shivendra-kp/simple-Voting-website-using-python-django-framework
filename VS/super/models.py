
from django.db import models
from elections.models import Constituency

# Create your models here.

class VoterIdCount(models.Model):
    region = models.OneToOneField(Constituency, on_delete=models.CASCADE)
    count = models.IntegerField(default=10001)

