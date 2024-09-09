from .import views
from django.urls import path

urlpatterns = [    
    path('', views.home_view, name='HomePage'),
    path('login/', views.LoginPage, name='login'),
    path('signup/', views.SignupPage, name='signup'),
    path('news/', views.fetch_news, name='fetch_news'),
    path('General Practitioner', views.Doctors, name='Doctors'),
]

    
