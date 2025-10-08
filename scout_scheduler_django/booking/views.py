from django.shortcuts import render, redirect
from django.urls import reverse
from .forms import BookingForm
from .api import ApiClient

def book(request):
    api=ApiClient()
    banner='New customers – Call us to set up your account!'
    if request.method=='POST':
        f=BookingForm(request.POST)
        if f.is_valid():
            cd=f.cleaned_data
            lookup=api.find_customer(cd['customer_first_name'],cd['customer_last_name'],cd['phone'])
            if not lookup['found']:
                f.add_error('phone','Customer not found.')
            else:
                ref=api.submit_appointment_request(cd)['ref']
                return redirect(reverse('success',kwargs={'ref':ref}))
    else: f=BookingForm()
    return render(request,'book.html',{'form':f,'banner':banner})

def success(request,ref): return render(request,'success.html',{'ref':ref})
