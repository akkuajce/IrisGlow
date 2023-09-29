from django.shortcuts import render
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect
from .models import CustomUser
from .decorators import user_not_authenticated
from .models import CustomUser,UserProfile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages

from django.shortcuts import redirect
from django.contrib.auth import logout


User = get_user_model()

# Create your views here.
def index(request):
    user=request.user
    if request.user.is_authenticated:
        if request.user.role == 4 and not request.path == reverse('admindashboard'):
            return redirect(reverse('admindashboard'))
        elif request.user.role == 2 and not request.path == reverse('doctor'):
            return redirect(reverse('doctordashboard'))
        elif request.user.role == 1 and not request.path == reverse('index'):
            return redirect(reverse('index'))
    
    return render(request,'index.html',)
def about(request):
    return render(request,'about.html',)
def appointment(request):
    return render(request,'appointment.html',)
def testimonial(request):
    return render(request,'testimonial.html',)
def doctorregister(request):
    return render(request,'doctorregister.html',)
def admindashboard(request):
    return render(request,'admindashboard.html',)
# def login(request):
#     return render(request,'login.html',)
# def register(request):
#     return render(request,'register.html',)



#login & Registration
# def userlogin(request):
#     if request.method == 'POST':
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(email)  # Print the email for debugging
#         print(password)  # Print the password for debugging

#         if email and password:
#             user = authenticate(request, email=email, password=password)
#             print("Authenticated user:", user)  # Print the user for debugging
#             if user is not None:
#                 auth_login(request, user)
#                 print("User authenticated:", user.email, user.role)
#                 if request.user.role == CustomUser.CLIENT:
#                     print("user is client")
#                     return redirect('http://127.0.0.1:8000/')
#                 elif request.user.role == CustomUser.THERAPIST:
#                     print("user is therapist")
#                     return redirect(reverse('therapist'))
#                 elif request.user.role == CustomUser.ADMIN:
#                     print("user is admin")                   
#                     return redirect(reverse('adminindex'))
#                 else:
#                     print("user is normal")
#                     return redirect('http://127.0.0.1:8000/')

#             else:
#                 error_message = "Invalid login credentials."
#                 return render(request, 'login.html', {'error_message': error_message})
#         else:
#             error_message = "Please fill out all fields."
#             return render(request, 'login.html', {'error_message': error_message})

#     return render(request, 'login.html')

# @user_not_authenticated
# def register(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name', None)
#         last_name = request.POST.get('last_name', None)
#         email = request.POST.get('email', None)
#         phone = request.POST.get('phone', None)
#         password = request.POST.get('pass', None)
#         confirm_password = request.POST.get('cpass', None)
#         role = User.CLIENT

#         if first_name and last_name and email and phone and password and role:
#             if User.objects.filter(email=email).exists():
#                 error_message = "Email is already registered."
#                 return render(request, 'register2.html', {'error_message': error_message})
            
#             elif password!=confirm_password:
#                 error_message = "Password's Don't Match, Enter correct Password"
#                 return render(request, 'register2.html', {'error_message': error_message})

            
#             else:
#             #     else:
#                 user = User(first_name =first_name,last_name=last_name, email=email, phone=phone,role=role)
#                 user.set_password(password)  # Set the password securely
#                 user.is_active=False
#                 user.save()
#                 user_profile = UserProfile(user=user)
#                 user_profile.save()
#                 # activateEmail(request, user, email)
#                 return redirect('login')  
            
#     return render(request, 'register2.html')


# login

def login_view(request):

    if request.user.is_authenticated:
        user=request.user
        if user.role == CustomUser.ADMIN:
            return redirect(reverse('admindashboard'))
        elif user.role == CustomUser.PATIENT:
                    return redirect(reverse('index'))
        elif user.role == CustomUser.DOCTOR:
                    return redirect(reverse('doctordashbord'))
        else:
                    return redirect('/')
      
    
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email,password)

        if email and password:
            user = authenticate(request, email=email, password=password)
            print("authenticated")

            if user is not None:
               
                auth_login(request, user)
                # Redirect based on user_type
                if user.role == CustomUser.ADMIN:
                    return redirect(reverse('admindashboard'))
                elif user.role == CustomUser.PATIENT:
                    return redirect(reverse('index'))
                elif user.role == CustomUser.DOCTOR:
                    return redirect(reverse('doctordashbord'))
                else:
                    return redirect('/')
                
            else:
                return HttpResponseRedirect(reverse('login') + '?alert=invalid_credentials')
        else:
            return HttpResponseRedirect(reverse('login') + '?alert=fill_fields')

    # For GET requests or if authentication fails, display the login form
    return render(request, 'login.html')
def userLogout(request):
    logout(request)
    return redirect('http://127.0.0.1:8000/') 

# def userLogout(request):
#     logout(request)
#     return redirect('index')

# Registration
def register(request):
    if request.user.is_authenticated:
        messages.warning(request, 'You are already logged in!')
        return redirect('index')
     

    elif request.method == 'POST':
        
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        confirmPassword = request.POST.get('confirmPassword', None)
        role = CustomUser.PATIENT

        if  first_name and last_name and email and phone and password and role:


            if User.objects.filter(email=email).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=email_is_already_registered')

            elif User.objects.filter(phone=phone).exists():
                return HttpResponseRedirect(reverse('register') + '?alert=phone_no_is_already_registered')
            
            elif password != confirmPassword: 
                return HttpResponseRedirect(reverse('register') + '?alert=passwords_do_not_match')
                

            else:
                user = User(first_name=first_name, last_name=last_name, email=email, phone=phone, role=role)
                user.set_password(password)  # Set the password securely
                user.save()

                user_profile = UserProfile(user=user)
                user_profile.save()
                return HttpResponseRedirect(reverse('login') + '?alert=registered')

    return render(request, 'register.html')

# Doctor Registration
# def doctorregister(request):
#     if request.method == 'POST':
#         first_name = request.POST.get('first_name', None)
#         last_name = request.POST.get('last_name', None)
#         username = request.POST.get('username', None)
#         email = request.POST.get('email', None)
#         phone = request.POST.get('phone', None)
#         password = request.POST.get('password', None)
#         confirmPassword = request.POST.get('confirmPassword', None)
#         user_type = CustomUser.DOCTOR

#         if username and first_name and last_name and email and phone and password and user_type:

#             if User.objects.filter(username=username).exists():
#                 return HttpResponseRedirect(reverse('register') + '?alert=username_is_already_registered')

#             elif User.objects.filter(email=email).exists():
#                 return HttpResponseRedirect(reverse('register') + '?alert=email_is_already_registered')

#             elif User.objects.filter(phone_no=phone).exists():
#                 return HttpResponseRedirect(reverse('register') + '?alert=phone_no_is_already_registered')
            
#             elif password != confirmPassword: 
#                 return HttpResponseRedirect(reverse('register') + '?alert=passwords_do_not_match')
                

#             else:
#                 user = User(username=username, first_name=first_name, last_name=last_name, email=email, phone_no=phone,user_type=user_type)
#                 user.set_password(password)  # Set the password securely
#                 user.save()

#                 user_profile = UserProfile(user=user)
#                 user_profile.save()
#                 return HttpResponseRedirect(reverse('login') + '?alert=registered')

#     return render(request, 'doctorregister.html')