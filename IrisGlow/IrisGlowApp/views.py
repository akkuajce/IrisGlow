from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect

from DoctorApp.models import Appointments, Specialities

from .forms import BootstrapDateInput, BootstrapSelect, BootstrapTextInput, CustomUserForm, SpecialityForm, UserProfileForm
from .models import CustomUser
from .decorators import user_not_authenticated
from .models import CustomUser,UserProfile
from django.contrib.auth import get_user_model
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import never_cache
from social_django.models import UserSocialAuth
from social_django.utils import psa

from django.contrib.auth.models import User

from django.views.decorators.csrf import csrf_protect


# Your view code here



from django.shortcuts import redirect
from django.contrib.auth import logout

from django.views.decorators.csrf import csrf_protect


User = get_user_model()

# Create your views here.

@csrf_protect
def index(request):
    user=request.user
    if request.user.is_authenticated:
        if request.user.role == 4 and not request.path == reverse('admindashboard'):

            return redirect(reverse('admindashboard'))
        elif request.user.role == 2 and not request.path == reverse('doctordashboard'):
            return redirect(reverse('doctordashboard'))
        elif request.user.role == 1 and not request.path == reverse('index'):
            return redirect(reverse('index'))
        

    return render(request,'index.html',)
def about(request):
    return render(request,'about.html',)
# def team(request):
#     return render(request,'team.html',)

def doctor1(request):
    return render(request, 'teams/doctor1.html')

def doctordashboard(request):
    return render(request,'doctordashboard.html',)


def testimonial(request):
    return render(request,'testimonial.html',)
def contact(request):
    return render(request,'contact.html',)
def service(request):
    return render(request,'service.html',)
def cataract(request):
    return render(request,'cataract.html',)
def gloucoma(request):
    return render(request,'gloucoma.html',)
def diabeticretinopathy(request):
    return render(request,'diabeticretinopathy.html',)

def doctorregister(request):
    return render(request,'doctorregister.html',)
def admindashboard(request):
    user=request.user
    if request.user.is_authenticated:
        if request.user.role == 4 and not request.path == reverse('admindashboard'):
            return redirect(reverse('admindashboard'))
        elif request.user.role == 2 and not request.path == reverse('doctor_dashboard'):
            return redirect(reverse('doctor_dashboard'))
        elif request.user.role == 1 and not request.path == reverse('index'):
            return redirect(reverse('index'))
    else:
         return redirect(reverse('index'))   
    return render(request,'admindashboard.html',)





# def password_reset_complete(request):
#     return render(request,'password_reset_complete.html',)
# def password_reset_confirm(request):
#     return render(request,'password_reset_confirm.html',)
# def password_reset_done(request):
#     return render(request,'password_reset_done.html',)
# def password_reset_email(request):
#     return render(request,'password_reset_email.html',)
# def password_reset_form(request):
#     return render(request,'password_reset_form.html',)




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
# @csrf_protect



def login_view(request):

    if request.user.is_authenticated:
        user=request.user
       

        if user.role == CustomUser.ADMIN:
            messages.success(request, 'Login Success!!')
            return redirect(reverse('admindashboard'))
        elif user.role == CustomUser.PATIENT:
            messages.warning(request, 'Login Success!!')    
            return redirect(reverse('index'))
        elif user.role == CustomUser.DOCTOR:
            messages.success(request, 'Login Success!!')
            return redirect(reverse('doctordashboard'))
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
                    return redirect(reverse('doctordashboard'))
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
@csrf_protect
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




    # users = UserProfile.objects.all()  # Fetch all user profiles from the database
    # context = {'users': users}
    # return render(request, 'userdata.html', context)




#edit profile


@login_required
def profile(request):
    
    user = request.user

    # Initialize variables for user profile and therapist info
    user_profile = None
 
    if user.userprofile.user.role == 1:
        try:
            # Get the user profile information
            user_profile = UserProfile.objects.get(user=user.userprofile.user)
           
        except UserProfile.DoesNotExist:
            user_profile = None
            

    context = {
        'user': user,
        'user_profile': user_profile,  # User profile information
    }

    return render(request, 'patients/profile.html', context)




@csrf_protect
@login_required
def editprofile(request):
    user_id = request.user.id
    user = CustomUser.objects.get(id=user_id)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            user_profile_form.save()
            return redirect('profile')  # Redirect to the user's profile page after editing

    else:
        user_form = CustomUserForm(instance=user)
        user_profile_form = UserProfileForm(instance=user_profile)
    print(user_profile.profile_picture)
    context = {
        'user_form': user_form,
        'user_profile_form': user_profile_form,
        'user_profile':user_profile
    }

    return render(request, 'patients/edit-profile.html', context)

########################################################################################################################

#Update password

########################################################################################################################


@login_required
def change_password_patient(request):
    val = 0
    
    if request.method == 'POST':
        # Get the current user
        user = CustomUser.objects.get(email=request.user.email)
        
        # Get the new password and confirm password from the request
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        # Check if the passwords are empty
        if not new_password or not confirm_password:
            messages.error(request, 'Please fill in both password fields.')
            val = 2
        else:
            # Check if the passwords match
            if new_password == confirm_password:
                # Change the user's password
                user.set_password(new_password)
                user.save()
                # Update the session and log the user back in
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated.')
                val = 1
            else:
                messages.error(request, 'Passwords do not match.')

    return render(request, 'patients/profile.html', {'msg': val})





#user data view
def display_user_data(request):
    users = CustomUser.objects.filter(~Q(is_superuser=True), is_active=True)
    inactive_users = CustomUser.objects.filter(~Q(is_superuser=True), is_active=False)
    return render(request, 'userdata.html', {'users': users,'inactive_users':inactive_users})

#update status

# def updateStatus(request,update_id):
#     updateUser=User.objects.get(id=update_id)
# def updateStatus(request, update_id):
#     updateUser = CustomUser.objects.get(id=update_id)
#     if updateUser.is_active==True:
#         updateUser.is_active=False
#     else:
#         updateUser.is_active=True
#     updateUser.save()
    
#     return redirect('userdata')



# The activation and deactivation of user accounts and mail sending for reason


from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.shortcuts import redirect

#  update status views.py
def updateStatus(request, user_id):
    updateUser = CustomUser.objects.get(id=user_id)
    if updateUser.is_active:
        updateUser.is_active = False
    else:
        updateUser.is_active = True
    updateUser.save()
    reason = "Your account has been activated for a specific reason." if updateUser.is_active else "Your account has been deactivated for a specific reason."  # Set your specific reason here
    send_deactivation_email(updateUser, reason)
    return redirect('deactivated_users')  # Or redirect to the appropriate page

# View for displaying deactivated users
def deactivated_users(request):
    deactivated_users = CustomUser.objects.filter(is_active=False)
    return render(request, 'deactivated_users.html', {'deactivated_users': deactivated_users})

# View for deactivating a user
def deactivate_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_active = False
    user.save()
    reason = "Your account has been deactivated for not using the account for more than 1 month."  # Set your specific reason here
    send_deactivation_email(user, reason)
    return redirect('deactivated_users')


#to activate users

def activate_user(request, user_id):
    user = CustomUser.objects.get(id=user_id)
    user.is_active = True
    user.save()
    reason = "Your account has been activated for a specific reason."  # Set your specific reason here
    send_activation_email(user, reason)
    return redirect('deactivated_users')


# Import your CustomUser model
from .models import CustomUser

# Send Activation Email Function
def send_activation_email(user, reason):
    subject = 'Account Activation'
    message = render_to_string('activation_email.html', {'reason': reason})
    from_email = 'irisgloweyecare@gmail.com'  # Your email address
    to_email = user.email

    email = EmailMessage(subject, message, from_email, [to_email])
    email.content_subtype = "html"
    email.send()

# Send Deactivation Email Function


def send_deactivation_email(user, reason):
    subject = 'Account Deactivation'
    message = render_to_string('deactivation_email.html', {'reason': reason})
    from_email = 'irisgloweyecare@gmail.com'  # Your email address
    to_email = user.email

    email = EmailMessage(subject, message, from_email, [to_email])
    email.content_subtype = "html"
    email.send()






def patient_appointment(request):
    doctor = request.user
    appointments = Appointments.objects.filter(therapist=doctor)

    # Group appointments by date using Python code
    grouped_appointments = {}
    for appointment in appointments:
        date = appointment.date
        if date not in grouped_appointments:
            grouped_appointments[date] = []
        grouped_appointments[date].append(appointment)

    # Sort the grouped appointments by date
    sorted_grouped_appointments = dict(sorted(grouped_appointments.items()))

    context = {
        'doctor': doctor,
        'grouped_appointments': sorted_grouped_appointments,
    }

    return render(request, 'patients/patient_appointment.html', context)










# Create your views here.
@login_required
def addSpeciality(request):
    if request.method == 'POST':
        form = SpecialityForm(request.POST)
        if form.is_valid():
            speciality_name = form.cleaned_data['speciality_name']
            symptoms = form.cleaned_data['symptoms']
            diagnosis = form.cleaned_data['diagnosis']
            treatments = form.cleaned_data['treatments']
            
            # Check if a therapy with the same name already exists
            if Specialities.objects.filter( speciality_name=speciality_name).exists():
                error_message = "Speciality with this name already exists."
            else:
                therapy = Specialities.objects.create(speciality_name=speciality_name, symptoms=symptoms, diagnosis=diagnosis, treatments=treatments)
                therapy.save()
                return redirect('index')  # Redirect to the index page after successful registration
        else:
            error_message = "Form is not valid."
    else:
        form = SpecialityForm()
        error_message = None

    return render(request, 'specialities.html', {'form': form, 'error_message': error_message})
