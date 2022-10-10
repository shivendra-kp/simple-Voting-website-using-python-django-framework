from argparse import ONE_OR_MORE
from asyncio.windows_events import NULL
from pyexpat import model
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User


# Create your models here.
class Constituency(models.Model):
    name = models.CharField(max_length=50 )
    state= models.CharField(max_length=50 , default="")
    union= models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.name + " ," + self.state


class PendingRegistrations(models.Model):
    user = models.OneToOneField(User , on_delete=models.CASCADE,primary_key=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    dob = models.DateField()
    fathers_name = models.CharField(max_length=60)
    mothers_name = models.CharField(max_length=60)
    adhaar_num = models.CharField(max_length=16)

    #Regional Data
    region = models.OneToOneField(Constituency,on_delete=models.SET_NULL , null=True)
    def __str__(self) -> str:
        return self.user.name



class Party(models.Model):
    name = models.CharField(max_length=50)
    short_name = models.CharField(max_length=10 , default="")
    formed = models.DateField()
    party_logo = models.ImageField(null= True , blank=True , default="defaults/partylogo.png" , upload_to="partylogo/")

    def __str__(self) -> str:
        return self.name
 

class Candidate(models.Model):
    party = models.ForeignKey(Party , on_delete=models.SET_NULL , null = True , blank=True)
    name = models.CharField(max_length= 50)
    constituency = models.ForeignKey(Constituency, on_delete=models.SET_NULL, null = True, blank=True )

    def __str__(self) -> str:
        return self.name

class Election(models.Model):
    name = models.CharField(max_length=30)
    class Status(models.TextChoices):
        HIDDEN = 'hidden', _('Hidden')
        IDLE = 'idle', _('Idle')
        RUNNING = 'running', _('Running')
        FINISHED = 'finished', _('Finished')
        PUBLISHED = 'published', _('Published')
        ARCHIVED = 'archived', _('Archived')

    status = models.CharField(max_length=20, choices=Status.choices , default=Status.HIDDEN)

    regions = models.ManyToManyField(Constituency ,null = True , blank=True)
    candidates = models.ManyToManyField(Candidate , null = True , blank=True)
    parties = models.ManyToManyField(Party , null = True , blank=True)
    

    def __str__(self) -> str:
        return self.name



class Voted(models.Model):
    election = models.ForeignKey(Election,on_delete=models.CASCADE)
    vid = models.CharField(max_length=20)

    def __str__(self) -> str:
        return self.election.name + " " +self.vid


class ElectionResults(models.Model):
    election = models.ForeignKey(Election,on_delete=models.CASCADE , default=NULL , null=True)
    party = models.ForeignKey(Party,on_delete=models.CASCADE , default=NULL , null=True)
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE , default=NULL , null=True)
    region = models.ForeignKey(Constituency,on_delete=models.CASCADE , default=NULL , null=True)
    votes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.election.name + " | " +  self.region.name + " | " +self.candidate.name + " | " + self.party.name


class BB(models.Model):
    election = models.ForeignKey(Election,on_delete=models.CASCADE)
    candidate = models.ForeignKey(Candidate,on_delete=models.CASCADE , null=True, blank=True)
    lh = models.CharField(max_length=80)
    h= models.CharField(max_length=80)


