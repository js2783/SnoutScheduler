from django.db import models

class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name  = models.CharField(max_length=100)
    phone      = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('first_name', 'last_name', 'phone')

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"

class Booking(models.Model):
    
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    pet_name = models.CharField(max_length=100, blank=True, null=True)
    #This will not allow for double bookings with the same groomer/date/time.
    class Meta:
        unique_together = ('groomer_id', 'appointment_date', 'appointment_time')

    
    services = models.JSONField(default=list, blank=True)

    groomer_id = models.IntegerField(null=True, blank=True)
    appointment_date = models.DateField(null=True, blank=True)
    appointment_time = models.CharField(max_length=20, blank=True, null=True)

    api_ref = models.CharField(max_length=100, blank=True, null=True)  
    api_payload = models.JSONField(default=dict, blank=True)            
    api_response = models.JSONField(default=dict, blank=True)           

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking {self.id} — {self.customer or 'Unknown customer'} on {self.appointment_date} at {self.appointment_time}"