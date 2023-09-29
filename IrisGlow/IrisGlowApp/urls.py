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
    path('doctorregister/', views.doctorregister, name='doctorregister'), 
    path('admindashboard/', views.admindashboard, name='admindashboard'), 
    path('logout/', views.userLogout, name='logout'), 
       
]