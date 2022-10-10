
from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login ,logout

from elections.models import Constituency,Election,Candidate,Voted,ElectionResults
from .forms import RegistrationForm, VoterSignupForm
from .models import UserData
from .forms import ResultsFilter
from django.db.models import Q

from operator import itemgetter
from super.blockchain import mine_block,get_blockchain

# Create your views here.

block = ""


def home(request):
    if request.user.is_authenticated:
        if request.user.is_superuser:
            return redirect('admin-home')
        return redirect('voter-home')
    context = {}
    return render(request,'base/home.html', context)





def voterlogin(request):
    
    context = {}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']


        user = authenticate(username = username, password = password)

        if user is not None:
            login(request,user)
            if user.is_superuser:
                return redirect('admin-home')
            return redirect('voter-home')
        else:
            print("Login View")
            if not (username==''or password==''):
                context['error'] = "username or password is incorrect."
 
    return render(request,'base/voter_login.html', context)


def voterlogout(request):
    if 'usermeta' in request.session:
        del request.session['usermeta']
    
    context = {}
    logout(request)
    return redirect('home')


def votersignup(request):
    print("Signin View")

    form = VoterSignupForm(request.POST or None)
    error = ""
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['password']
        pass2 = request.POST['cpassword']
        
        valid = True
        
        #enter your checks here
        if User.objects.filter(username=username).exists():
            error = 'username already exists'
            valid = False 
        elif pass1 != pass2 :
            valid = False
            error = "passwords doesn't match"
        
        if valid:
            myuser = User.objects.create_user(username, email, pass1)
            myuser.save()
            
            login(request , myuser)
            return redirect('voter-home')


    context = {'form' : form ,'error' : error}
    return render(request,'base/voter_signup.html', context)


def voterhome(request):
    user = request.user
    userdata=UserData.objects.filter(user=user).first()
    elections = None
    voted = {}
    if userdata:
        request.session['usermeta']={'username':userdata.first_name ,'vid':userdata.voter_id , 'profile_pic_url': userdata.profile_pic.url}
        if userdata.registration_status == 'approved':
            elections = Election.objects.filter(regions=userdata.region).filter(~Q(status='archived') or ~Q(status='hidden'))
            
            for election in elections:
                if Voted.objects.filter(election = election).filter(vid = userdata.voter_id).exists():
                    voted[election.id] = True
                else:
                    voted[election.id] = False
 
    context = {'user':user, 'userdata':userdata ,'elections':elections ,'home' : True , 'voted' : voted}
    context['page'] = 'home'
    
    return render(request,'base/voter_home.html',context)



def verificationform(request):
    form = RegistrationForm(request.POST or None)
    
    if request.method == 'POST':
        
        userdata = UserData.objects.filter(user=request.user).first()
        if userdata == None:
            #no old userdata found
            userdata = UserData(user=request.user)

        post = request.POST
        userdata.first_name = post['first_name']
        userdata.last_name = post['last_name']
        userdata.dob = post['dob']
        userdata.father_name = post['father_name']
        userdata.mother_name = post['mother_name']
        userdata.adhaar_number = post['adhaar_number']
        userdata.mobile_number = post['mobile_number']
        userdata.region = Constituency.objects.get(id = post['region'])

        #verify all the data
        is_valid=True

        
        if is_valid:
            userdata.registration_status = 'pending'
            userdata.save()
            return redirect('voter-home')
        
    else:
        #Pre saved data
        userdata = UserData.objects.filter(user=request.user).first()
        if userdata != None:
            print(userdata.first_name)
            forminit= {
                'first_name': userdata.first_name,
                'last_name': userdata.last_name,
                'dob': userdata.dob,
                'father_name': userdata.father_name,
                'mother_name': userdata.mother_name,
                'adhaar_number': userdata.adhaar_number,
                'mobile_number': userdata.mobile_number,
                'region': userdata.region
            }

            form = RegistrationForm(initial=forminit)


    context = {'form':form}
    return render(request,'base/verification_form.html',context)


def castvote(request,eid):
    election = Election.objects.get(id=eid)
    
    userdata = UserData.objects.get(user=request.user)

    candidates = election.candidates.filter(constituency=userdata.region)

    context = {'election':election , 'candidates':candidates , 'region':userdata.region}
    return render(request ,'base/cast_vote.html',context)


def oncastvote(request,eid,cid):
    election = Election.objects.get(id=eid)
    candidate= Candidate.objects.get(id=cid)
    userdata = UserData.objects.get(user=request.user)

    voted = Voted.objects.filter(election = election , vid = userdata.voter_id).first()
    if voted is None:
        #add voting data to blockchain.
        last_block = get_blockchain(election).last()
        mine_block(last_block , election , candidate)

        voted = Voted(election = election , vid = userdata.voter_id)
        voted.save()
    else:
        print("You Have already voted- cant vote again")
        return redirect('voter-home')

    res = ElectionResults.objects.filter(election=election , party= candidate.party , candidate=candidate , region=candidate.constituency).first()

    if res != None:
        res.votes+=1
    else:
        res = ElectionResults(election=election , party= candidate.party , candidate=candidate , region=candidate.constituency)
        res.votes+=1
    print(res)
    res.save()
    


    print("Voter ID" + userdata.voter_id + " === Election :" + election.name + " --> Candidate : " + candidate.name)

    return redirect('voter-home')


def viewresults(request,eid):
    election = Election.objects.get(id=eid)
    ftr = ''
    results =[]

    if request.method == 'GET':
        ftr = request.GET.get('choice')
        if ftr == None:
            ftr = 'overall'

    eres = ElectionResults.objects.filter(election=election)
    filterform = ResultsFilter()

    votes =None
    parties =None
    regions = None

    if ftr == 'overall':
        if request.session.has_key(eid + '_res_overall'):
            results = request.session[eid + '_res_overall']

        else:
            temp = {}

            #tie is not included
            for region in election.regions.all():
                win = {'party_id': '' , 'votes' : 0}
                for party in election.parties.all():
                    ob = eres.filter(region = region , party=party).first()
                    if ob is None:
                        print("Not Found")
                        break
                    if party.id in temp:
                        temp[party.id][0] += ob.votes
                        temp[party.id][2] += 1
                        
                    else:
                        #[total votes , wins , participated , party]
                        temp[party.id] = [ob.votes,0,1 , party.name, party.party_logo.url]
                    
                    if win['votes'] < ob.votes:
                        win['party_id'] = party.id
                        win['votes'] = ob.votes
                
                temp[win['party_id']][1] += 1
            
            results = []
            for value in temp.values():
                results.append(value)
            
                request.session[eid + '_res_overall'] = results
    
    if ftr == 'region':
        if request.session.has_key(eid + '_res_region'):
            results = request.session[eid + '_res_region']

        else:
            temp={}
            for region in election.regions.all():
                temp[region.id] = [region.name, region.state, region.union,[]]
                _list = eres.filter(region=region)
                for ob in _list:
                    t = [ ob.party.name, ob.party.party_logo.url, ob.votes, ob.candidate.name]
                    temp[region.id][3].append(t)

                sorted(temp[region.id][3], key=itemgetter(2))

                
            for value in temp.values():
                results.append(value)
        
        request.session[eid + '_res_region'] = results
     

    if ftr == 'candidate':
        if request.session.has_key(eid + '_res_candidate'):
            results = request.session[eid + '_res_candidate']

        else:
            temp={}
            for party in election.parties.all():
                temp[party.id] = [party.name,party.party_logo.url,[]]
                _list = eres.filter(party=party)
                for ob in _list:
                    t=[ob.candidate.name, ob.region.name,ob.votes]
                    temp[party.id][2].append(t)
            
            for value in temp.values():
                results.append(value)
        
        request.session[eid + '_res_candidate'] = results


    context={'filter' : ftr,'filterform': filterform,'election': election , 'results' : results}
    context['page'] = 'election-results'
    return render(request, 'base/view_results.html',context)



def voteredit(request):
    context={'page':'edit'}
    if request.method =='POST':
        return redirect('voter-home')
    return render(request,'base/edit_profile.html',context)

def voternews(request):
    context={'page':'news'}
    return render(request,'base/news.html',context)

def temp(request):
    context={}
    return render(request,'base/temp.html',context)