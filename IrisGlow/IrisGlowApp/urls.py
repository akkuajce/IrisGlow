from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
# from django.contrib.auth import views as auth_views

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
    path('change_password_patient/', views.change_password_patient, name='change_password_patient'),
    # path('toggle_status/<int:user_id>/', views.toggle_user_status, name='toggle_user_status'),
    # path('deactivated_users/', views.deactivated_users_list, name='deactivated_users_list'),
    # path('userdata/', views.userdata, name='usersata'),
    path('updateStauts/<int:update_id>',views.updateStatus,name="updateStatus"),


    path('deactivated-users/', views.deactivated_users, name='deactivated_users'),
    path('activate-user/<int:user_id>/', views.activate_user, name='activate_user'),
    #google authentication
    # path('social-auth/', include('social_django.urls', namespace='social')),
     path("", include("allauth.urls")), #most important
    

    


#password reset urls

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_email/', auth_views., name='password_reset_email'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  

]