from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from datetime import datetime
from .models import Doctor, PatientProfile, Appointment
from django.core.exceptions import ValidationError
import requests
from django.utils.dateparse import parse_date
import logging
from django.urls import reverse
from django.contrib import messages
import pytz
from django.core.exceptions import ValidationError
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import colors
import os
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from .models import *
from django.contrib.auth import logout
from datetime import datetime, timedelta, date
from .models import BlogPost, Doctor, ClinicHours, Appointment, PatientProfile

#home
def home(request):
    return render(request, 'homepage.html')

#logout
def logout_view(request):
    logout(request)
    return redirect('signup')

#about_us_page
def about_us(request):
    return render(request, 'about_us.html')

#medix_bot
def chat_with_medix(request):
    return render(request, 'chat_with_medix.html')

#login_page
def LoginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            print("Redirecting to home page...")
            return redirect('home')
        else:
            return HttpResponse("Username or Password is incorrect!")

    return render(request, 'login.html')

#signup_page
def SignupPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password')
        password2 = request.POST.get('confirmPassword')

        if password1 != password2:
            return HttpResponse("Your password and confirm password do not match.")
        
        if User.objects.filter(username=username).exists():
            return HttpResponse("Username already exists.")
        if User.objects.filter(email=email).exists():
            return HttpResponse("Email already registered.")

        User.objects.create_user(username=username, email=email, password=password1)
        return redirect('login')

    return render(request, 'signup.html')

#live_news_fetch
def fetch_news(request):
    api_key = '421d25b85f06645b73a653c33eefd5e5'
    url = f'https://gnews.io/api/v4/top-headlines?country=in&category=health&token={api_key}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        articles = response.json().get('articles', [])
    except requests.exceptions.RequestException as e:
        print(f"Error fetching news: {e}")
        articles = []

    return render(request, 'new_list.html', {'articles': articles})


def orthopedic_doctor(request):
    return render(request, 'Orthopedic Doctor.html')


def ent_specialist(request):
    return render(request, 'ENT Specialist.html')


def dermatologist(request):
    return render(request, 'Dermatologist.html')


def general_practitioner(request):
    return render(request, 'General Practitioner.html')


def general_practitioner2(request):
    return render(request, 'general practitioner2.html')


def pediatrician(request):
    return render(request, 'Pediatrician.html')


def gynecologist(request):
    return render(request, 'Gynecologist.html')


def gynecologist2(request):
    return render(request, 'gynecologist2.html')

#display_all_doctors_in_carousel
def Doctors(request):
    return render(request, 'Doctors.html')


def BMI(request):
    return render(request, 'BMI calculator.html')


def PeriodTracker(request):
    return render(request, 'Period calculator.html')


def CalorieCounter(request):
    return render(request, 'Calorie Counter.html')


def LabsDiagnostics(request):
    return render(request, 'Labs&Diagnostics.html')


def HomecareServices(request):
    return render(request, 'Homecare Services.html')


def NutritionalCounselling(request):
    return render(request, 'Nutritional Counseling.html')


def PreventiveCare(request):
    return render(request, 'preventic care.html')

def HealthWorkshops(request):
    return render(request, 'health workshops.html')


def appointmentSchedule(request):
    return render(request, 'appointment shedulling service.html')

#inhouse_doctor_blogs
def blog_list(request):
    blogs = BlogPost.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})


#side_panel_for_blogs
def blog_detail(request, blog_id):
    blog = get_object_or_404(BlogPost, id=blog_id)
    other_posts = BlogPost.objects.exclude(id=blog_id).order_by('-created_at')[:5]  #display at max 5 blogs in sidepanel
    return render(request, 'blog_detail.html', {
        'blog': blog,
        'other_posts': other_posts
    })

#book an appointment page
def book_appointment(request):
    if request.method == 'GET':
        doctors = Doctor.objects.all()
        try:
            patient_profile = PatientProfile.objects.get(user=request.user)
            first_name = request.user.first_name
            last_name = request.user.last_name
        except PatientProfile.DoesNotExist:
            patient_profile = None
            first_name = request.user.first_name
            last_name = request.user.last_name
        
        return render(request, 'book_appointment.html', {
            'doctors': doctors,
            'patient_profile': patient_profile,
            'first_name': first_name,
            'last_name': last_name
        })

    elif request.method == 'POST':
        doctor_id = request.POST.get('doctor')
        date_str = request.POST.get('date')
        time_slot_str = request.POST.get('time_slot')

    if not (doctor_id and date_str and time_slot_str):
        return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_slot = datetime.strptime(time_slot_str, '%H:%M').time()

        # Get the patient profile
        patient_profile = PatientProfile.objects.get(user=request.user)

        # Create the appointment
        appointment = Appointment(
            doctor_id=doctor_id,
            date=date_obj,
            time_slot=time_slot,
            patient_profile=patient_profile  #link the patient profile
        )

        appointment.clean()  # Ensure validation
        appointment.save()

        # Return success response and redirect URL
        return JsonResponse({'success': True, 'redirect_url': reverse('view_profile', args=[patient_profile.id])})

    except PatientProfile.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Patient profile not found.'}, status=404)
    except ValidationError as e:
        return JsonResponse({'success': False, 'error': e.messages}, status=400)
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
    

#render available time slots from backend   
def get_available_time_slots(request):
    doctor_id = request.GET.get('doctor_id')
    date_str = request.GET.get('date')

    if doctor_id and date_str:
        try:
            doctor = Doctor.objects.get(id=doctor_id)
            clinic_hours = doctor.clinic_hours
        except Doctor.DoesNotExist:
            return JsonResponse({'available_slots': []})

        available_slots = []
        weekday = datetime.strptime(date_str, '%Y-%m-%d').weekday()

        if weekday < 5:  # Monday to Friday
            start = clinic_hours.monday_to_friday_start
            end = clinic_hours.monday_to_friday_end
        elif weekday == 5:  # Saturday
            start = clinic_hours.saturday_start
            end = clinic_hours.saturday_end
        else:  # Sunday
            if not (clinic_hours.sunday_start and clinic_hours.sunday_end):
                return JsonResponse({'available_slots': []})
            start = clinic_hours.sunday_start
            end = clinic_hours.sunday_end

        if isinstance(start, str):
            start = datetime.strptime(start, '%H:%M').time()
        if isinstance(end, str):
            end = datetime.strptime(end, '%H:%M').time()

        current_time = datetime.combine(datetime.today(), start)
        end_time = datetime.combine(datetime.today(), end)

        while current_time.time() <= end_time.time():
            if not Appointment.objects.filter(doctor=doctor, date=date_str, time_slot=current_time.time()).exists():
                available_slots.append(current_time.strftime('%H:%M'))
            current_time += timedelta(minutes=30)  # divide time slots into 30 mins intervals

        return JsonResponse({'available_slots': available_slots})

    return JsonResponse({'available_slots': []})


#generate a downloadable pdf with appointment details
def generate_appointment_pdf(request, appointment_id):
    appointment = get_object_or_404(Appointment, id=appointment_id)

    # Create a PDF response
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="appointment_{appointment_id}.pdf"'

    # Create a PDF document
    doc = SimpleDocTemplate(response, pagesize=letter)

    elements = []

    # Define styles
    styles = getSampleStyleSheet()
    title_style = styles['Title']
    heading_style = styles['Heading2']
    normal_style = styles['Normal']

    # Add title and details to the PDF
    elements.append(Paragraph("Medix", title_style))
    elements.append(Paragraph("Appointment Confirmation", heading_style))
    elements.append(Spacer(1, 12)) 

    details = [
        ('Patient Name', appointment.patient_name),
        ('Doctor', appointment.doctor.name),
        ('Date', appointment.date.strftime('%Y-%m-%d')),
        ('Time Slot', appointment.time_slot.strftime('%H:%M'))
    ]

    for label, value in details:
        elements.append(Paragraph(f"<b>{label}:</b> {value}", normal_style))
        elements.append(Spacer(1, 12)) 

    elements.append(Paragraph("<strong>Note:</strong> Please arrive at the clinic 15 minutes before your scheduled time to avoid any delays.", normal_style))
    elements.append(Spacer(1, 12))

    if hasattr(appointment, 'additional_info') and appointment.additional_info:
        elements.append(Paragraph(f"<b>Additional Info:</b> {appointment.additional_info}", normal_style))
        elements.append(Spacer(1, 12)) 

    doc.build(elements)
    return response


#create profile of patient logged in
def view_or_create_profile(request, id):
    user = get_object_or_404(User, id=id)
    profile, created = PatientProfile.objects.get_or_create(
        user=user,
        defaults={
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
        }
    )


    # Fetch appointments for the patient profile with specified patient id
    appointments = Appointment.objects.filter(patient_profile=profile)

    return render(request, 'profile.html', {'profile': profile, 'appointments': appointments})


#view the patient profile
def view_profile(request, id):
    profile = get_object_or_404(PatientProfile, id=id)
    return render(request, 'profile.html', {'profile': profile})


#edit profile details
def edit_profile(request, id):
    profile = get_object_or_404(PatientProfile, id=id)
    
    if request.method == 'POST':
        # Extract and validate form data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        street_address = request.POST.get('street_address')
        city = request.POST.get('city')
        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')
        blood_group = request.POST.get('blood_group')
        gender = request.POST.get('gender')
        marital_status = request.POST.get('marital_status')

        # Validate and save profile data
        try:
            if date_of_birth:
                parsed_date = parse_date(date_of_birth)
                if parsed_date is None:
                    raise ValidationError("Invalid date format.")
                profile.date_of_birth = parsed_date
            profile.first_name = first_name
            profile.last_name = last_name
            profile.email = email
            profile.phone_number = phone_number
            profile.street_address = street_address
            profile.city = city
            profile.state = state
            profile.postal_code = postal_code
            profile.blood_group = blood_group
            profile.gender = gender
            profile.marital_status = marital_status
            profile.save()

            
            print(f"Redirecting to profile/{profile.id}")

            return redirect('view_profile', id=profile.id)
        except ValidationError as e:
            return render(request, 'edit_profile.html', {'profile': profile, 'error': str(e)})

    return render(request, 'edit_profile.html', {'profile': profile})


#view previous reports of the patient
def view_previous_reports(request):
    documents = Document.objects.filter(user=request.user)
    return render(request, 'previous_reports.html', {'documents': documents})

#feedback or contact us
def contact_us(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        comment = request.POST.get('text')

        # Validate the form data
        if not (name and email and comment):
            return JsonResponse({'success': False, 'error': 'All fields are required.'}, status=400)

        # Create a new ContactUs entry
        contact_entry = ContactUs(name=name, email=email, comment=comment)
        contact_entry.save()

        # Add a success message
        messages.success(request, 'Your message has been sent successfully!')
        return redirect('home') 

    return render(request, 'contact_us.html')