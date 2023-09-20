from django.shortcuts import render
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect
from .decorators import user_not_authenticated
from django.contrib.auth import get_user_model
from .models import CustomUser,UserProfile

User = get_user_model()


# Create your views here.

def index(request):
    return render(request,'index.html',)
def about(request):
    return render(request,'about.html',)
def appointment(request):
    return render(request,'appointment.html',)
def login(request):
    return render(request,'login.html',)
@user_not_authenticated
def register(request):
    if request.method == 'POST':
        f_name = request.POST.get('first_name', None)
        l_name = request.POST.get('last_name', None)
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        confirm_password = request.POST.get('confirmPassword', None)
        role = User.PATIENT

        if f_name and l_name and email and phone and password and role:
            if User.objects.filter(email=email).exists():
                error_message = "Email is already registered."
                return render(request, 'register2.html', {'error_message': error_message})
            
            elif password!=confirm_password:
                error_message = "Password's Don't Match, Enter correct Password"
                return render(request, 'register2.html', {'error_message': error_message})

            
            else:
                user = User(first_name=f_name,last_name=l_name, email=email, phone=phone,role=role)
                user.set_password(password)  # Set the password securely
                user.is_active=True
                user.save()
                user_profile = UserProfile(user=user)
                user_profile.save()
                return redirect('login')  
            
    return render(request, 'register.html')
def testimonial(request):
    return render(request,'testimonial.html',)
#  def login(request):
#     return render(request,'login.html',)
def userlogin(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        print(email)  
        print(password)  

        if email and password:
            user = authenticate(request, email=email, password=password)
            print("Authenticated user:", user)  
            if user is not None:
                auth_login(request, user)
                print("User authenticated:", user.email, user.role)
                if request.user.role == CustomUser.PATIENT:
                    print("user is client")
                    return redirect('http://127.0.0.1:8000/')
                elif request.user.role == CustomUser.DOCTOR:
                    print("user is therapist")
                    return redirect(reverse('therapist'))
                elif request.user.role == CustomUser.ADMIN:
                    print("user is admin")                   
                    return redirect(reverse('adminindex'))
                else:
                    print("user is normal")
                    return redirect('http://127.0.0.1:8000/')

            else:
                error_message = "Invalid login credentials."
                return render(request, 'login.html', {'error_message': error_message})
        else:
            error_message = "Please fill out all fields."
            return render(request, 'login.html', {'error_message': error_message})

    return render(request,'login.html')