from django import forms
from .api import ApiClient
class BookingForm(forms.Form):
    customer_first_name = forms.CharField(max_length=50)
    customer_last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=25)
    pet_name = forms.CharField(max_length=50)
    services = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    groomer = forms.ChoiceField()
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    appointment_time = forms.ChoiceField()
    def __init__(self,*a,**kw):
        super().__init__(*a,**kw)
        api=ApiClient()
        self.fields['services'].choices=[(str(s['id']),s['name']) for s in api.list_services()]
        self.fields['groomer'].choices=[(str(g['id']),g['name']) for g in api.list_groomers()]
        self.fields['appointment_time'].choices=[(t,t) for t in api.list_time_slots('')]
