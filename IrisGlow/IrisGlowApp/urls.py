from django.contrib import admin
from django.urls import include, path
from django.contrib.auth import views as auth_views
from . import views
from .views import appointment_list, doctor_list, payment_list
from .views import frame_list, frame_detail, edit_frame, delete_frame
from .views import remove_from_cart, add_to_cart, view_cart





# from django.contrib.auth import views as auth_views

urlpatterns = [

    path('remove_from_cart/<int:frame_id>/', remove_from_cart, name='remove_from_cart'),
    path('add_to_cart/<int:frame_id>/', add_to_cart, name='add_to_cart'),
    path('cart/', view_cart, name='cart'),
    

    path('wishlist/', views.view_wishlist, name='wishlist'),
    path('add_to_wishlist/<int:frame_id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('remove_from_wishlist/<int:frame_id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('update_cart/<int:frame_id>/', views.update_cart, name='update_cart'),
    # path('update_cart_quantity/', views.update_cart_quantity, name='update_cart_quantity'),


    path('checkout/', views.checkout, name='checkout'),


    




    


    path('',views.index,name='index'),

    path('about/', views.about, name='about'),



    path('spects_change_password/', views.spects_change_password, name='spects_change_password'),
    path('spects_edit_profile/', views.spects_edit_profile, name='spects_edit_profile'),
    path('spects/view-profile/', views.spects_view_profile, name='spects_view_profile'),


    
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


    path('add_product/', views.add_product, name='add_product'),


    path('frame-list/', frame_list, name='frame_list'),
    path('frame-detail/<int:frame_id>/', frame_detail, name='frame_detail'),
    path('frames/<int:frame_id>/edit/', edit_frame, name='edit_frame'),
    path('frames/<int:frame_id>/delete/', delete_frame, name='delete_frame'),


    path('frame-details-common/<int:frame_id>/', views.frame_details_common_view, name='frame_details_common'),

    path('payment2/<int:shipping_address_id>/', views.payment2, name='payment2'),
    path('paymenthandler2/<int:shipping_address_id>/', views.paymenthandler2, name='paymenthandler2'),

    path('order-details/', views.order_details, name='order_details'),

    


    # path('generate_order_summary_pdf/<int:order_id>/', views.generate_order_summary_pdf, name='generate_order_summary_pdf'),




    # path('add_to_cart/<int:frame_id>/', add_to_cart, name='add_to_cart'),
    # path('cart/', cart_view, name='cart'),
    # path('get_cart_data/', views.get_cart_data, name='get_cart_data'),
    # path('remove_from_cart/<int:frame_id>/', views.remove_from_cart, name='remove_from_cart'),





    




    




    



     

    

   


#password reset urls

    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    # path('password_reset_email/', auth_views., name='password_reset_email'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),  

]