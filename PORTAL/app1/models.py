from django.db import models
from django.contrib.auth.models import User
import datetime
from ckeditor.fields import RichTextField
from django.core.exceptions import ValidationError
from datetime import datetime
from django.core.exceptions import ValidationError
from datetime import datetime



class Article(models.Model):
    author = models.CharField(max_length=100)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    url = models.URLField()
    urlToImage = models.URLField(null=True, blank=True)
    publishedAt = models.DateTimeField()
    content = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title


class PatientProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_of_birth = models.DateField(default='2000-01-01')
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    street_address = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    profile_picture = models.ImageField(upload_to='profile_pictures', null=True, blank=True)
    blood_group = models.CharField(max_length=3, choices=[
        ('A+', 'A+'),
        ('A-', 'A-'),
        ('B+', 'B+'),
        ('B-', 'B-'),
        ('AB+', 'AB+'),
        ('AB-', 'AB-'),
        ('O+', 'O+'),
        ('O-', 'O-'),
    ], default='O+')
    gender = models.CharField(max_length=10, choices=[
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ], default='O') 
    
    marital_status = models.CharField(max_length=10, choices=[
        ('Single', 'Single'),
        ('Married', 'Married'),
        
    ], default='Single') 


    def __str__(self):
        return f"{self.first_name} {self.last_name}'s Profile"
    


class BlogPost(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()
    image = models.ImageField(upload_to='blog_images', null=True, blank=True)
    author=models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    


class ClinicHours(models.Model):
    doctor = models.OneToOneField('Doctor', on_delete=models.CASCADE, related_name='clinic_hours')
    monday_to_friday_start = models.TimeField()
    monday_to_friday_end = models.TimeField()
    saturday_start = models.TimeField(null=True, default=None)
    saturday_end = models.TimeField(null=True, default=None)
    sunday_start = models.TimeField(null=True, default=None)  # Set a default value
    sunday_end = models.TimeField(null=True, default=None)    # Set a default value

    def __str__(self):
        return f"{self.doctor.name} Clinic Hours"
    

        
class Doctor(models.Model):
    name = models.CharField(max_length=100)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Appointment(models.Model):
    patient_profile = models.ForeignKey(PatientProfile, on_delete=models.CASCADE, null=True) 
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time_slot = models.TimeField()
    patient_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.patient_name} - {self.doctor.name} on {self.date} at {self.time_slot}"

    def clean(self):
        super().clean()
        
        # Fetch clinic hours related to the doctor 
        try:
            clinic_hours = ClinicHours.objects.get(doctor=self.doctor)
        except ClinicHours.DoesNotExist:
            raise ValidationError("Clinic hours for the selected doctor are not set.")

        # Weekday validation (Monday to Friday)
        if self.date.weekday() < 5:  # Monday to Friday
            if not (clinic_hours.monday_to_friday_start <= self.time_slot <= clinic_hours.monday_to_friday_end):
                raise ValidationError("Selected time is outside of clinic hours for this doctor.")

        # Saturday validation
        elif self.date.weekday() == 5:  # Saturday
            if not (clinic_hours.saturday_start <= self.time_slot <= clinic_hours.saturday_end):
                raise ValidationError("Selected time is outside of clinic hours on Saturday.")

        # Sunday validation
        else:  # Sunday
            if clinic_hours.sunday_start is None or clinic_hours.sunday_end is None:
                raise ValidationError("The clinic is closed on Sundays.")
            elif not (clinic_hours.sunday_start <= self.time_slot <= clinic_hours.sunday_end):
                raise ValidationError("Selected time is outside of clinic hours on Sunday.")

        # Check if the time slot is already booked
        if Appointment.objects.filter(doctor=self.doctor, date=self.date, time_slot=self.time_slot).exists():
            raise ValidationError("This time slot is already booked. Please choose a different slot.")
        

        
class Document(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    file = models.FileField(upload_to='documents/')
    description = models.TextField(blank=True, null=True)  # Add description field
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.file.name} uploaded by {self.user.username} on {self.uploaded_at}"
    
    
    
class ContactUs(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name