from .import views
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static

urlpatterns = [
        
    path('home/', views.home, name='home'),
    path('about/', views.about_us, name='about_us'),
    path('login/', views.LoginPage, name='login'),
    path('', views.SignupPage, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('news/', views.fetch_news, name='fetch_news'),
    path('orthopedic-doctor/', views.orthopedic_doctor, name='orthopedic_doctor'),
    path('ent-specialist/', views.ent_specialist, name='ent_specialist'), 
    path('dermatologist/', views.dermatologist, name='dermatologist'), 
    path('general-practitioner/', views.general_practitioner, name='general_practitioner'),
    path('general-practitioner2/', views.general_practitioner2, name='general_practitioner2'), 
    path('pediatrician/', views.pediatrician, name='pediatrician'), 
    path('gynecologist/', views.gynecologist, name='gynecologist'),
    path('gynecologist2/', views.gynecologist2, name='gynecologist2'),
    path('calculate-BMI/', views.BMI, name='calculate-BMI'),
    path('period-tracker/', views.PeriodTracker, name='period-tracker'),
    path('calorie-counter/', views.CalorieCounter, name='calorie-counter'), 
    path('labs-diagnostics/', views.LabsDiagnostics, name='labs_diagnostics'),
    path('homecare-services/', views.HomecareServices, name='homecare_services'),
    path('nutritional-counseling/', views.NutritionalCounselling, name='nutritional_counseling'),
    path('preventive-care/', views.PreventiveCare, name='preventive_care'),
    path('health-workshops/', views.HealthWorkshops, name='health_workshops'),
    path('appointment-scheduling/', views.appointmentSchedule, name='appointment_scheduling'),        
    path('profile/<int:id>/', views.view_or_create_profile, name='view_profile'),
    path('profile/<int:id>/edit/', views.edit_profile, name='edit_profile'),
    path('appointment/<int:appointment_id>/pdf/', views.generate_appointment_pdf, name='generate_appointment_pdf'),    
    path('blogs/', views.blog_list, name='blog_list'),
    path('blogs/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('book-appointment/', views.book_appointment, name='book_appointment'),
    path('doctors/', views.Doctors, name='doctor-list'),
    path('get-available-time-slots/', views.get_available_time_slots, name='get_available_time_slots'),
    path('appointments/pdf/<int:appointment_id>/', views.generate_appointment_pdf, name='generate_appointment_pdf'),
    path('previous-reports/', views.view_previous_reports, name='previous_reports'),
    path('chat/', views.chat_with_medix, name='chat_with_medix'),
    path('contact/', views.contact_us, name='contact_us'),
    
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    

    
