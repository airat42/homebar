from django import forms
from cocktails.models import Client

class CreateForm(forms.Form):
    client = forms.ModelChoiceField(label="Кто заказывает?", queryset=Client.objects.all())
    class Meta:
        model = Client
        fields = ['client',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['client'].widget.attrs.update({'class': 'myform'})