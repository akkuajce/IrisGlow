from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
   
    path('add-doctor/',views.addDoctor,name='addDoctor'),
    
    path('team/', views.doctor, name='team'),
    path('view-doctor/<int:user_id>/',views.viewdoctor,name='view-doctor'),

    path('doctor_dashboard/', views.doctor_dashboard, name='doctor_dashboard'),
    

    # ... other URL patterns ...

    # URL for viewing a doctor's profile
   
    # URL for editing a doctor's profile
    path('doctorprofile/', views.doctorprofile, name='doctorprofile'),
    path('editdoctorprofile/', views.editdoctorprofile, name='editdoctorprofile'),


    path('appointment/<int:t_id>/', views.appointment, name='appointment'),
    path('get-available-time-slots/', views.get_available_time_slots, name='get-available-time-slots'),


    # urls.py
path('view-appointments/', views.view_appointments, name='view-appointments'),

]

   
    
