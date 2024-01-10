from django import forms
from cocktails.models import Clients

class CreateForm(forms.Form):
    client = forms.ModelChoiceField(label="Кто заказывает?", queryset=Clients.objects.all())
    class Meta:
        model = Clients
        fields = ['client',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].widget.attrs.update({'class': 'myform'})