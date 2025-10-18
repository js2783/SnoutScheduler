from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from .forms import BookingForm
from .api import ApiClient
from .models import Customer, Booking
from django.db import transaction
from django.core.paginator import Paginator
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages

def book(request):
    api = ApiClient()
    banner = 'New customers – Call us to set up your account!'

    # Prepare all available time slots for the template
    all_time_slots = api.list_time_slots('')

    if request.method == 'POST':
        f = BookingForm(request.POST)
        if f.is_valid():
            cd = f.cleaned_data  # This is the clean data after validation

            try:
                services = [int(s) for s in cd.get('services', [])]
            except ValueError:
                f.add_error('services','Invalid service selection.')
                return render(request,'booking/book.html',{'form':f,'banner':banner,'all_time_slots':all_time_slots})

            groomer_id = None      #Converts groomer ID to an integer
            if cd.get('groomer'):
                try:
                    groomer_id = int(cd['groomer'])
                except ValueError:
                    f.add_error('groomer','Invalid groomer selection.')
                    return render(request,'booking/book.html',{'form':f,'banner':banner,'all_time_slots':all_time_slots})

            appt_date = cd.get('appointment_date')
            appt_time = cd.get('appointment_time')

            # Check for double booking
            if groomer_id is not None and appt_date and appt_time:
                conflict_qs = Booking.objects.filter(
                    groomer_id=groomer_id,
                    appointment_date=appt_date,
                    appointment_time=appt_time
                )
                if conflict_qs.exists():
                    f.add_error(None, "That groomer already has a booking at the selected date and time. Please choose another time or groomer.")
                    return render(request,'booking/book.html',{'form':f,'banner':banner,'all_time_slots':all_time_slots})

            try:
                lookup = api.find_customer(cd['customer_first_name'], cd['customer_last_name'], cd['phone'])
            except Exception as exc:
                f.add_error(None, f'Error checking customer: {exc}')
                return render(request,'booking/book.html',{'form':f,'banner':banner,'all_time_slots':all_time_slots})

            if not lookup.get('found'):
                f.add_error('phone', 'Customer not found. Please call to set up an account.')
                return render(request,'booking/book.html',{'form':f,'banner':banner,'all_time_slots':all_time_slots})
            #Prepares to submit the appointment to the API
            payload = {
                "customer_first_name": cd['customer_first_name'],
                "customer_last_name": cd['customer_last_name'],
                "phone": cd['phone'],
                "pet_name": cd.get('pet_name'),
                "service_ids": services,
                "groomer_id": groomer_id,
                "appointment_date": appt_date.isoformat() if appt_date else None,
                "appointment_time": appt_time,
            }

            try:
                result = api.submit_appointment_request(payload)
            except Exception as exc:
                f.add_error(None, f"Could not submit appointment: {exc}")
                return render(request,'booking/book.html',{'form':f,'banner':banner,'all_time_slots':all_time_slots})

            ref = result.get('ref')
            if not ref:
                f.add_error(None, "Appointment created but server did not return a reference.")
                return render(request,'booking/book.html',{'form':f,'banner':banner,'all_time_slots':all_time_slots})
            #Saves the booking
            try:
                with transaction.atomic():
                    customer_obj, created = Customer.objects.get_or_create(
                        first_name=cd['customer_first_name'],
                        last_name=cd['customer_last_name'],
                        phone=cd['phone']
                    )
                    booking_obj = Booking.objects.create(
                        customer=customer_obj,
                        pet_name=cd.get('pet_name'),
                        services=services,
                        groomer_id=groomer_id,
                        appointment_date=appt_date,
                        appointment_time=appt_time,
                        api_ref=ref,
                        api_payload=payload,
                        api_response=result,
                    )
            except Exception as exc:
                f.add_error(None, f"Saved remotely but failed to save locally: {exc}")
                return render(request,'booking/book.html',{'form':f,'banner':banner,'all_time_slots':all_time_slots})
                #Redirects to the success page. 
            return redirect(reverse('booking:success', kwargs={'ref': ref}))

    else:
        f = BookingForm()

    return render(request, 'booking/book.html', {
        'form': f,
        'banner': banner,
        'all_time_slots': all_time_slots,  # Pass to template
    })

#This will show the user that there booking request was successful.
def success(request, ref):
    return render(request,'booking/success.html',{'ref':ref})


def bookings_list(request):
    # show most recent first
    qs = Booking.objects.select_related('customer').order_by('-appointment_date', '-appointment_time', '-created_at')
    

    # Allows the user to see 25 appointments per page. Can be adjusted to however many we want.
    paginator = Paginator(qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'booking/bookings_list.html', {'page_obj': page_obj})

def booking_detail(request, pk):
    booking = get_object_or_404(Booking.objects.select_related('customer'), pk=pk)
    
    api = ApiClient()

    # Map groomer ID to name
    groomers = {str(g['id']): g['name'] for g in api.list_groomers()}
    booking.groomer_name = groomers.get(str(booking.groomer_id), "—")

    # Map service IDs to names
    services_lookup = {str(s['id']): s['name'] for s in api.list_services()}
    booking.services_names = [services_lookup.get(str(sid), f"Service {sid}") for sid in booking.services]

    # Do NOT expose raw API response
    

    return render(request, 'booking/booking_detail.html', {'booking': booking})

def availability_json(request):
    groomer = request.GET.get('groomer')
    date = request.GET.get('date')
    booked = []
    if groomer and date:
        booked = list(Booking.objects.filter(groomer_id=int(groomer), appointment_date=date).values_list('appointment_time', flat=True))
    return JsonResponse({'booked': booked})

def bookings_list(request):
    qs = Booking.objects.select_related('customer').order_by('-appointment_date', '-appointment_time', '-created_at')
    paginator = Paginator(qs, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    
    api = ApiClient()
    groomer_lookup = {str(g['id']): g['name'] for g in api.list_groomers()}

    # attach a groomer_name property to each booking
    for b in page_obj.object_list:
        b.groomer_name = groomer_lookup.get(str(b.groomer_id), f"Groomer {b.groomer_id or '—'}")
#This returns the JSON with all the booked times that were inputted. 
    return render(request, 'booking/bookings_list.html', {'page_obj': page_obj})

@require_POST
def cancel_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)

    # Prefer a soft-cancel
    if hasattr(booking, "canceled"):
        if booking.canceled:
            messages.info(request, "This booking is already canceled.")
        else:
            booking.canceled = True
            if hasattr(booking, "canceled_at"):
                booking.canceled_at = timezone.now()
            # update only fields that exist
            fields = ["canceled"] + (["canceled_at"] if hasattr(booking, "canceled_at") else [])
            booking.save(update_fields=fields)
            messages.success(request, "Booking canceled.")
    elif hasattr(booking, "status"):
        if getattr(booking, "status") == "canceled":
            messages.info(request, "This booking is already canceled.")
        else:
            booking.status = "canceled"
            if hasattr(booking, "canceled_at"):
                booking.canceled_at = timezone.now()
            fields = ["status"] + (["canceled_at"] if hasattr(booking, "canceled_at") else [])
            booking.save(update_fields=fields)
            messages.success(request, "Booking canceled.")
    else:
        # Hard delete as last resort
        booking.delete()
        messages.warning(request, "Successfully Cancelled Appointment!")

    # Go back to the list (or use hidden input 'next' if provided)
    return redirect(request.POST.get("next") or "booking:list")

def edit_booking(request, pk):
    booking = get_object_or_404(Booking, pk=pk)
    if request.method == 'POST':
        form = BookingForm(request.POST, instance=booking)
        if form.is_valid():
            form.save()
            return redirect('booking:list')
    else:
        form = BookingForm(instance=booking)
    return render(request, 'booking/book.html', {'form': form})