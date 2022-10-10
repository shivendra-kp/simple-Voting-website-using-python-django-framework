from django.contrib import admin
from . models import BB, Election, Party , Candidate, Constituency ,PendingRegistrations,Voted,ElectionResults

# Register your models here.
# admin.site.register(Election)
# admin.site.register(Party)
# admin.site.register(Candidate)
admin.site.register(Constituency)
# admin.site.register(PendingRegistrations)
# admin.site.register(Voted)
# admin.site.register(ElectionResults)
# admin.site.register(BB)