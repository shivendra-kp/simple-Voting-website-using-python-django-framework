from django.forms import ModelForm
from .models import Election, Party,Candidate



class ElectionForm(ModelForm):
    class Meta:
        model = Election
        fields = ['name']


class PartyForm(ModelForm):
    class Meta:
        model = Party
        fields = ['name','short_name','formed','party_logo']

        def __init__(self, *args, **kwargs):
            super(PartyForm, self).__init__(*args, **kwargs)
            self.fields['name'].label = "Party Name"

class CandidateForm(ModelForm):
    class Meta:
        model = Candidate
        fields = ['name','party','constituency']