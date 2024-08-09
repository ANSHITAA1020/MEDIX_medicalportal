from .import views
from django.urls import path

urlpatterns = [
    path('', views.HomePage, name='home'),
    path('login/', views.LoginPage, name='login'),
    path('signup/', views.SignupPage, name='signup'),

    
]