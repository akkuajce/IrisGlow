from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .views import appointment_list, doctor_list, payment_list




# from django.contrib.auth import views as auth_views

urlpatterns = [
    path('',views.index,name='index'),

    path('about/', views.about, name='about'),
    
    path('buyframes/', views.buyframes, name='buyframes'),
    path('eyeglasses/', views.eyeglasses, name='eyeglasses'),
    path('sunglasses/', views.sunglasses, name='sunglasses'),
    path('computerglasses/', views.computerglasses, name='computerglasses'),



    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('testimonial/', views.testimonial, name='testimonial'),
    # path('team/', views.team, name='team'),
    path('doctor1/', views.doctor1, name='doctor1'),
    path('service/', views.service, name='service'),
    path('cataract/', views.cataract, name='cataract'),
    path('gloucoma/', views.gloucoma, name='gloucoma'),
    path('diabeticretinopathy/', views.diabeticretinopathy, name='diabeticretinopathy'), 

    path('contact/', views.contact, name='contact'),
    # path('doctorregister/', views.doctorregister, name='doctorregister'),
    path('doctordashboard/', views.doctordashboard, name='doctordashboard'), 
    path('admindashboard/', views.admindashboard, name='admindashboard'), 
    path('logout/', views.userLogout, name='logout'), 
    # path('team/', views.team, name='team'),
    path('userdata/', views.display_user_data, name='userdata'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.editprofile, name='edit-profile'),
    path('change_password_patient/', views.change_password_patient, name='change_password_patient'),
    # path('toggle_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    # path('deactivated_users/', views.deactivated_users_list, name='deactivated_users_list'),
    # path('userdata/', views.userdata, name='usersata'),
    # path('updateStauts/<int:update_id>',views.updateStatus,name="updateStatus"),
    path('update-status/<int:user_id>/', views.updateStatus, name='updateStatus'),


    path('deactivated-users/', views.deactivated_users, name='deactivated_users'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    #google authentication
    # path('social-auth/', include('social_django.urls', namespace='social')),
     path("", include("allauth.urls")), #most important


     path('patient-appointment/', views.patient_appointment, name='patient_appointment'),


     path('addSpeciality/', views.addSpeciality, name='addSpeciality'),


    path('appointment-list/', appointment_list, name='appointment-list'),
    path('payment-list/', payment_list, name='payment-list'),



    path('patient_appointment_history/', views.patient_appointment_history, name='patient_appointment_history'),


    path('admin/', admin.site.urls),
    path('doctor-list/', views.doctor_list, name='doctor_list'),





    path('add_spects/', views.add_spects, name='add_spects'),
    path('success_page/', views.success_page, name='success_page'),

    # Assuming you have a URL for Spects Dashboard named 'spects_dashboard'
    path('spects_dashboard/', views.spects_dashboard, name='spects_dashboard'),




    




    




    



     

    

   


#password reset urls

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_email/', auth_views., name='password_reset_email'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  

]