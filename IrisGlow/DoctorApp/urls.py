from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views



urlpatterns = [
   
    path('add-doctor/',views.addDoctor,name='addDoctor'),
    
    path('team/', views.doctor, name='team'),
    path('view-doctor/<int:user_id>/',views.viewdoctor,name='view-doctor'),

    path('doctordashboard/', views.doctor_dashboard, name='doctordashboard'),
    

    # ... other URL patterns ...

    # URL for viewing a doctor's profile
   
    # URL for editing a doctor's profile
    path('doctorprofile/', views.doctorprofile, name='doctorprofile'),
    path('editdoctorprofile/', views.editdoctorprofile, name='editdoctorprofile'),


    

    path('appointment/<int:t_id>/', views.appointment, name='appointment'),
    path('get-available-time-slots/', views.get_available_time_slots, name='get-available-time-slots'),
    path('appointment-confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment_confirmation'),


    # urls.py
    path('view-appointments/', views.view_appointments, name='view-appointments'),


    path('appointment-confirmation/<int:appointment_id>/', views.appointment_confirmation, name='appointment-confirmation'),

    path('doctor-list/', views.doctor_list, name='doctor-list'),

    path('search_doctor/', views.search_doctor, name='search_doctor'),



    path('doctor-day-off/', views.doctor_day_off, name='doctor_day_off'),
    path('doctor-day-off-confirmation/', views.doctor_day_off_confirmation, name='doctor_day_off_confirmation'),



#payment
path('payment/<int:appointment_id>/<str:t_fees>/', views.payment, name='payment'),
path('paymenthandler/<int:appointment_id>/', views.paymenthandler, name='paymenthandler'),



    






    

]

   
    
