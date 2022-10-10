from multiprocessing import context
from aiohttp import content_disposition_filename
from django.shortcuts import redirect, render
from django.db.models import Q
from base.models import UserData
from elections.models import Election
from elections.models import Party , Candidate , Election, ElectionResults
from elections.forms import PartyForm,CandidateForm,ElectionForm
from .utils import generatevid
import os
from .blockchain import add_genesis, get_blockchain

# Create your views here.


def adminhome(request):
    
 #   if not request.user.is_authenticated:
 #       print("Login Required")
 #       return redirect('/super/login')

    elections = Election.objects.filter(~Q(status='archived'))
    context = {'elections' : elections , 'show_elections' : True , 'page':'home'}
    return render(request,'super/admin_home.html',context)


def adminlogin(request):
    context = {}
    return render(request,'super/admin_login.html', context)


#ELECTION ACTIONS

def createelection(request):

    if request.method == 'POST':
        form = ElectionForm(request.POST)
        if form.is_valid():
            election = form.save()
            add_genesis(election)
            return redirect('admin-home')

    form = ElectionForm()

    context = {'form' : form , 'page':'create-election'}
    return render(request,'super/create_election.html', context)


def editelection(request,pk):
    election = Election.objects.get(id=pk)
    if request.method == 'POST':
        form = ElectionForm(request.POST, request.FILES, instance=election)
        form.save()
        return redirect('admin-home')


    form = ElectionForm(instance=election)
    candidates = election.candidates.all()

    context = {'form':form , 'candidates':candidates , 'election' : election}
    return render(request,'super/edit_election.html', context)


def deleteelection(request,pk):
    election = Election.objects.get(id=pk)
    for candidate in election.candidates.all():
        election.candidates.remove(candidate)
        candidate.delete()
    election.delete()
    return redirect('admin-home')


def startelection(request,pk):
    election = Election.objects.get(id=pk)
    election.status = 'running'
    election.save()
    return redirect('admin-home')


def endelection(request,pk):
    election = Election.objects.get(id=pk)
    election.status = 'finished'
    election.save()
    return redirect('admin-home')

def viewelection(request,pk):
    election = Election.objects.get(id=pk)
    chain = get_blockchain(election)
    context = {'blockchain':chain}
    return render(request,'super/view_election.html',context)


def publishelection(request,pk):
    election = Election.objects.get(id=pk)
    election.status = 'published'
    election.save()

    for candidate in election.candidates.all():
        if ElectionResults.objects.filter(election=election, candidate=candidate, party=candidate.party, region=candidate.constituency).exists():
            pass
        else:
            temp = ElectionResults(election=election, candidate=candidate, party=candidate.party, region=candidate.constituency, votes=0)
            temp.save()

    return redirect('admin-home')


def archiveelection(request,pk):
    election = Election.objects.get(id=pk)
    election.status = 'archived'
    election.save()
    return redirect('admin-home')



def makepublic(request,pk):
    election = Election.objects.get(id=pk)
    election.status = 'idle'
    election.save()
    return redirect('admin-home')

#PARTY ACTIONS

def createparty(request):
    if request.method == 'POST':
        form = PartyForm(request.POST , request.FILES)

        if form.is_valid():
            form.save()
            return redirect('manage-parties')
        else:
            print("Something Unexpected happened")

    form = PartyForm()
    context = {'form' : form} 
    return render(request,'super/create_party.html', context)


def editparty(request,pk):
    party = Party.objects.get(id=pk)
    if request.method == 'POST':
        print(request.POST)
        if bool(request.FILES):
            
            if request.FILES.get('party_logo')!= None and len(party.party_logo) > 0  and  not party.party_logo.url.startswith('/media/defaults/'):
                print("Image File is deleted")
                os.remove(party.party_logo.path)
        
        form = PartyForm(request.POST , request.FILES, instance=party) 
        form.save()
        return redirect('manage-parties')


    form = PartyForm(instance=party)
    context = {'form':form}
    return render(request,'super/edit_party.html', context)


def deleteparty(request,pk):
    party = Party.objects.get(id=pk)
    #delete old media and make sure to not delete default stuffs
    if len(party.party_logo) > 0  and  not party.party_logo.url.startswith('/media/defaults/'):
        os.remove(party.party_logo.path)

    
    party.delete()

    return redirect('manage-parties')
    

#CANDIDATE ACTIONS

def createcandidate(request,eid):
    error =""
    if request.method == 'POST':
        form = CandidateForm(request.POST , request.FILES)
        election = Election.objects.get(id=eid)
        candidate = form.save(commit=False)

        #validate candidates
        #each region has only on one candidate from one party
        if len(election.candidates.filter(party=candidate.party , constituency=candidate.constituency)) >0:
            error = "Can't have more than one candidate of same party in same region"

        if form.is_valid() and error == "":
            candidate.save()
            election.candidates.add(candidate) 

            if not election.regions.filter(id =candidate.constituency.id).exists():
                print('add region ' + candidate.constituency.name + ' to election : ' + election.name)
                election.regions.add(candidate.constituency)
            
            if not election.parties.filter(id =candidate.party.id).exists():
                print('add party ' + candidate.party.name + ' to election : ' + election.name)
                election.parties.add(candidate.party)
            
            return redirect('edit-election' ,eid)
  
    form = CandidateForm()
    context = {'form':form , 'error' : error}
    return render(request,'super/create_candidate.html', context)


def editcandidate(request,pk,eid):
    candidate = Candidate.objects.get(id=pk)
    election = Election.objects.get(id=eid)

    error = ''
    if request.method == 'POST':
        temp = Candidate.objects.get(id=pk)
        form = CandidateForm(request.POST , request.FILES ,instance=temp)
        old_region = candidate.constituency
        old_party = candidate.party
        cand = form.save(commit=False)
  

        if len(election.candidates.filter(party=cand.party , constituency=cand.constituency))>0:
            error = "Can't have more than one candidate of same party in same region"

        if cand.party == old_party and cand.constituency == old_region:
            error = ""
        
        if form.is_valid() and error == "":
            cand = form.save()
            #remove old region if no candiates in te given region
            if not len(election.candidates.filter(constituency=old_region)) > 0:
                print('delete region ' + old_region.name + ' from election : ' + election.name)
                election.regions.remove(old_region)
            
            if not len(election.candidates.filter(party=old_party)) > 0:
                print('delete party ' + old_party.name + ' from election : ' + election.name)
                election.parties.remove(old_party)

            #add new region to election if does not already exists
            if not election.regions.filter(id =cand.constituency.id).exists():
                print('add region ' + cand.constituency.name + ' to election : ' + election.name)
                election.regions.add(cand.constituency)


            if not election.parties.filter(id =cand.party.id).exists():
                print('add party ' + candidate.party.name + ' to election : ' + election.name)
                election.parties.add(candidate.party)

            return redirect('edit-election' ,eid)
    
    form = CandidateForm(instance=candidate)
    context = {'form':form , 'error' :error}
    return render(request,'super/edit_candidate.html', context)

def deletecandidate(request,pk ,eid):
    election = Election.objects.get(id=eid)
    candidate = Candidate.objects.get(id=pk)
    
    election.candidates.remove(candidate.id)

    old_region= candidate.constituency
    old_party = candidate.party
    candidate.delete()

    if not len(election.candidates.filter(constituency=old_region)) > 0:
                print('delete region ' + old_region.name + ' from election : ' + election.name)
                election.regions.remove(old_region)

    if not len(election.candidates.filter(party = old_party)) > 0:
                print('delete party ' + old_party.name + ' from election : ' + election.name)
                election.parties.remove(old_party)

    return redirect('edit-election' ,eid)




def managecandidates(request):
    context = {}
    return render(request,'super/manage_candidates.html', context)


def manageparties(request):
    parties = Party.objects.all()
    context = {'parties' : parties ,'page':'manage-parties'}
    return render(request,'super/manage_parties.html', context)


def vvl(request):
    voters = UserData.objects.filter(registration_status='pending')
    context = {"voters":voters ,'page':'vvl'}
    return render(request,'super/voter_verification_list.html', context)


def approvevoter(request,pk):
    userdata = UserData.objects.get(id=pk)
    userdata.voter_id = generatevid(userdata.region)
    userdata.registration_status = 'approved'
    userdata.save()
    return redirect ('voter-verification-list')

def denyvoter(request,pk):
    pass