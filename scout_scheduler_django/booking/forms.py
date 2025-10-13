from django import forms
from .models import Booking
from .api import ApiClient
from django.core.exceptions import ValidationError

class BookingForm(forms.Form):
    customer_first_name = forms.CharField(max_length=50)
    customer_last_name = forms.CharField(max_length=50)
    phone = forms.CharField(max_length=25)
    pet_name = forms.CharField(max_length=50, required=False)
    services = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple)
    groomer = forms.ChoiceField()
    appointment_date = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    appointment_time = forms.ChoiceField()

    def __init__(self, *a, **kw):
        super().__init__(*a, **kw)
        api = ApiClient()
        #This will populate each field with the list of groomers, services, and times that are available. 
        self.fields['services'].choices = [(str(s['id']), s['name']) for s in api.list_services()]
        self.fields['groomer'].choices = [(str(g['id']), g['name']) for g in api.list_groomers()]
        self.fields['appointment_time'].choices = [(t, t) for t in api.list_time_slots('')]
#This clean allows for the services to be validated when entered. It will show error if it does not validate. This covers each section and allows for no double bookings. 
    def clean_services(self):
        val = self.cleaned_data.get('services', [])
        try:
            return [int(v) for v in val]
        except ValueError:
            raise ValidationError("Invalid service id.")

    def clean_groomer(self):
        g = self.cleaned_data.get('groomer')
        try:
            return int(g)
        except (TypeError, ValueError):
            raise ValidationError("Invalid groomer selection.")

    def clean(self):
        cleaned = super().clean()
        groomer = cleaned.get('groomer')
        appt_date = cleaned.get('appointment_date')
        appt_time = cleaned.get('appointment_time')
        if groomer and appt_date and appt_time:
            # Check local DB for conflict
            if Booking.objects.filter(groomer_id=groomer, appointment_date=appt_date, appointment_time=appt_time).exists():
                raise ValidationError("That groomer already has a booking at the selected date and time.")
        return cleaned
    
    