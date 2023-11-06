
from datetime import datetime
from django.db import models
from IrisGlowApp.models import CustomUser

# Create your models here.
class Specialities(models.Model):
    speciality_name = models.CharField(max_length=100, unique=True)
    symptoms = models.TextField(blank=True, null=True)
    diagnosis = models.CharField(max_length=30)
    treatments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.speciality_name




class Doctor(models.Model):
    bio = models.TextField(blank=True, null=True)
    qualification = models.CharField(max_length=50, blank=True)
    license = models.CharField(max_length=100, unique=True)
    experience = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    speciality_name = models.ForeignKey(Specialities, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.email
    
    

#Appointment
from django.db import models
from datetime import datetime
#from accounts.models import CustomUser

class Appointments(models.Model):
    TIME_CHOICES = [
        (datetime.strptime('09:00 AM', '%I:%M %p').time(), '09:00 AM'),
        (datetime.strptime('11:00 AM', '%I:%M %p').time(), '11:00 AM'),
        (datetime.strptime('01:00 PM', '%I:%M %p').time(), '01:00 PM'),
        (datetime.strptime('03:00 PM', '%I:%M %p').time(), '03:00 PM'),
        (datetime.strptime('05:00 PM', '%I:%M %p').time(), '05:00 PM'),
    ]

    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
    ]

    date = models.DateField()
    client = models.ForeignKey(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='client_appointments',
        limit_choices_to={'role': CustomUser.DOCTOR}
    )
    therapist = models.ForeignKey(
        CustomUser,
        on_delete=models.CASCADE, 
        related_name='therapist_appointments',
        limit_choices_to={'role': CustomUser.DOCTOR}
    )
    time_slot = models.TimeField(choices=TIME_CHOICES)
    created_date = models.DateTimeField(auto_now_add=True,null=True)
    modified_date = models.DateTimeField(auto_now=True, null=True)
    cancelled_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
 
    def __str__(self):
        return f"Appointment with {self.client.first_name} and {self.therapist.first_name} on {self.date} at {self.get_time_slot_display()}"