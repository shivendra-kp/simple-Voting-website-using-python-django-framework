from distutils.command.upload import upload
from email.policy import default
from random import choices
from django import forms
from elections.models import Constituency

class VoterSignupForm(forms.Form):
    username = forms.CharField(label = 'Username', max_length = 50)
    email= forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput() , label='Password')
    cpassword = forms.CharField(widget=forms.PasswordInput() , label='Confirm Password')


class RegistrationForm(forms.Form):
    first_name = forms.CharField(max_length=15)
    last_name = forms.CharField(max_length=15)
    dob = forms.DateField()
    father_name = forms.CharField(max_length=35,)
    mother_name = forms.CharField(max_length=35)

    adhaar_number =forms.CharField(max_length=20 , widget=forms.NumberInput)
    mobile_number =forms.CharField(max_length=10,  widget=forms.NumberInput)

    region= forms.ModelChoiceField(queryset=Constituency.objects.all())

    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        self.fields['dob'].label = "Date of Birth (yyyy-mm-dd)"


FILTER_CHOICES = (
    ('party','party'),
    ('region','region'),
    ('candidate','candidate'),
)

class ResultsFilter(forms.Form):
    choice = forms.ChoiceField(choices=FILTER_CHOICES)

