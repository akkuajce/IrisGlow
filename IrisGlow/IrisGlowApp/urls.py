from django.contrib import admin
from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('',views.index,name='index'),

    path('about/', views.about, name='about'),
    path('appointment/', views.appointment, name='appointment'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('testimonial/', views.testimonial, name='testimonial'), 
    # path('doctorregister/', views.doctorregister, name='doctorregister'),
    path('doctordashboard/', views.doctordashboard, name='doctordashboard'), 
    path('admindashboard/', views.admindashboard, name='admindashboard'), 
    path('logout/', views.userLogout, name='logout'), 
    path('team/', views.team, name='team'),
    path('userdata/', views.display_user_data, name='userdata'),
    path('profile/', views.profile, name='profile'),
    path('edit_profile/', views.editprofile, name='edit-profile'),
    path('change_password_patients/', views.change_password_patients, name='change_password_patients'),
    


#password reset urls

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_email/', auth_views., name='password_reset_email'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  

]