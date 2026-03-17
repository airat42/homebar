from django import forms
from cocktails.models import Client, Ingridient

class CreateForm(forms.Form):
    drink = forms.ModelChoiceField(label="Что заказываем?", queryset=Ingridient.objects.filter(category__in=[1, 2]))
    class Meta:
        model = Ingridient
        fields = ['drink',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['drink'].widget.attrs.update({'class': 'myform'})