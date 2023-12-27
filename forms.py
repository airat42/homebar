from django import forms
from cocktails.models import Clients

class CreateForm(forms.Form):
    client = forms.ModelChoiceField(label="", queryset=Clients.objects.all())