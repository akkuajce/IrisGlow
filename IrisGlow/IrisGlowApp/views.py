import dataclasses
from decimal import Decimal
import json
from random import sample
from django.shortcuts import get_object_or_404, render
from django.contrib.auth import login as auth_login ,authenticate, logout
from django.shortcuts import render, redirect

from DoctorApp.models import Appointments, Specialities

from .forms import BootstrapDateInput, BootstrapSelect, BootstrapTextInput, CustomUserForm, SpecialityForm, UserProfileForm
from .models import CustomUser, PaymentP
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
        elif request.user.role == 3 and not request.path == reverse('spects_dashboard'):
            return redirect(reverse('spects_dashboard'))
        elif request.user.role == 1 and not request.path == reverse('index'):
            return redirect(reverse('index'))
        

    return render(request,'index.html',)

@login_required
def about(request):
    return render(request,'about.html',)
# def team(request):
#     return render(request,'team.html',)

@login_required
def doctor1(request):
    return render(request, 'teams/doctor1.html')






from django.db.models import Q
@login_required
def buyframes(request):
    query = request.GET.get('q')

    if query:
        # Perform search based on frame name or brand name
        frames = Frame.objects.filter(Q(name__icontains=query) | Q(brand_name__icontains=query))
    else:
        # Fetch a random selection of frames (adjust the number as needed)
        frames = sample(list(Frame.objects.all()), 4)

    context = {
        'random_frames': frames,
        'query': query,
    }

    return render(request, 'buyframes.html', context)





def eyeglasses(request):
    return render(request, 'eyeglasses/eyeglasses.html')

def sunglasses(request):
    return render(request, 'sunglasses/sunglasses.html')

def computerglasses(request):
    return render(request, 'computerglasses/computerglasses.html')







@login_required
def doctordashboard(request):
    return render(request,'doctordashboard.html',)

@login_required
def testimonial(request):
    return render(request,'testimonial.html',)

@login_required
def contact(request):
    return render(request,'contact.html',)

@login_required
def service(request):
    return render(request,'service.html',)


@login_required
def cataract(request):
    return render(request,'cataract.html',)

@login_required
def gloucoma(request):
    return render(request,'gloucoma.html',)

@login_required
def diabeticretinopathy(request):
    return render(request,'diabeticretinopathy.html',)

@login_required
def doctorregister(request):
    return render(request,'doctorregister.html',)


from django.shortcuts import render, redirect
# from django.contrib.auth.models import User  # Assuming you are using the built-in User model
from django.urls import reverse
@login_required
def admindashboard(request):
    if request.user.is_authenticated:
        user = request.user
        if user.role == 4 and not request.path == reverse('admindashboard'):
            return redirect(reverse('admindashboard'))
        elif user.role == 2 and not request.path == reverse('doctor_dashboard'):
            return redirect(reverse('doctor_dashboard'))
        elif user.role == 3 and not request.path == reverse('spects_dashboard'):
            return redirect(reverse('spects_dashboard'))
        elif user.role == 1 and not request.path == reverse('index'):
            return redirect(reverse('index'))
        else:
            # Get the count of active users
            active_user_count = User.objects.filter(is_active=True).count()
            
            # Get the count of deactivated users
            deactivated_user_count = User.objects.filter(is_active=False).count()

            # Pass counts to the template context
            context = {
                'active_user_count': active_user_count,
                'deactivated_user_count': deactivated_user_count,
            }

            return render(request, 'admindashboard.html', context)
    else:
        return redirect(reverse('index'))








def login_view(request):

    if request.user.is_authenticated:
        user=request.user
       
        if user.role == CustomUser.ADMIN:
            messages.success(request, 'Login Success!!')
            return redirect(reverse('admindashboard'))
        elif user.role == CustomUser.PATIENT:
            messages.warning(request, 'Login Success!!')    
            return redirect(reverse('index'))
        elif user.role == CustomUser.SPECTS:
            messages.warning(request, 'Login Success!!')    
            return redirect(reverse('spects_dashboard'))
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
                elif user.role == CustomUser.SPECTS: 
                    return redirect(reverse('spects_dashboard'))
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
@login_required
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
@login_required
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





@login_required
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










# appointment_list (admin panel)

from datetime import date
from django.shortcuts import render
from DoctorApp.models import Appointments

@login_required
def appointment_list(request):
    # Filter appointments for the current date and future dates
    appointments = Appointments.objects.filter(date__gte=date.today()).order_by('date', 'time_slot')

    context = {'appointments': appointments}
    return render(request, 'appointment_list.html', context)




# payment_list (admin panel)

from django.shortcuts import render
from DoctorApp.models import Payment

@login_required
def payment_list(request):
    payments = Payment.objects.all()
    context = {'payments': payments}
    return render(request, 'payment_list.html', context)







# views.py
from django.shortcuts import render
from DoctorApp.models import Appointments

@login_required
def patient_appointment_history(request):
    # Assuming the user is logged in and the user's appointments are related through a ForeignKey
    appointments = Appointments.objects.filter(client=request.user)
    return render(request, 'patients/patient_appointment_history.html', {'appointments': appointments})













# doctor_list views.py
from django.shortcuts import render
from DoctorApp.models import Doctor

@login_required
def doctor_list(request):
    doctors = Doctor.objects.all()
    return render(request, 'doctor_list.html', {'doctors': doctors})







# views.py 09/02 Add Spects

# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .forms import SpectsUserForm
# from django.core.mail import send_mail
# from django.template.loader import render_to_string
# from django.utils.html import strip_tags

# @login_required(login_url='login')  # Ensure that only logged-in admins can access this view
# def add_spects(request):
#     if request.method == 'POST':
#         form = SpectsUserForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.role = CustomUser.SPECTS
#             user.save()

#             # Send email to the Spects
#             subject = 'Welcome to YourApp!'
#             message = render_to_string('spects_welcome_email.html', {'user': user})
#             plain_message = strip_tags(message)
#             from_email = 'irisgloweyecare@gmail.com'  # Update with your email
#             to_email = [user.email]
#             send_mail(subject, plain_message, from_email, to_email, html_message=message)

#             # You can add additional logic or redirection here
#             return redirect('success_page')  # Update with the appropriate URL
#     else:
#         form = SpectsUserForm()

#     return render(request, 'admin/add_spects.html', {'form': form})



@csrf_protect
@login_required
def add_spects(request):
         

    if request.method == 'POST':
        
        first_name = request.POST.get('first_name', None)
        last_name = request.POST.get('last_name', None)
        
        email = request.POST.get('email', None)
        phone = request.POST.get('phone', None)
        password = request.POST.get('password', None)
        confirmPassword = request.POST.get('confirmPassword', None)
        role = CustomUser.SPECTS

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

    return render(request, 'admin/add_spects.html')




from django.shortcuts import render

def success_page(request):
    return render(request, 'success_page.html')  # Replace with your actual template





# Spects dashboard
# Assuming you have a URL for Spects Dashboard named 'spects_dashboard'
# from django.contrib.auth.decorators import login_required
# from .forms import UserProfileForm


# @login_required
# def spects_dashboard(request):
#     if request.user.is_authenticated:
#         user = request.user
#         if user.role == 3 and not request.path == reverse('spects_dashboard'):
#             return redirect(reverse('spects_dashboard'))
#         else:

#             form = UserProfileForm(instance=user.userprofile)

#             if request.method == 'POST':
#                 form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
#                 if form.is_valid():
#                     form.save()
#             # Your Spects dashboard logic here
#             return render(request, 'spects_dashboard.html')
#     else:
#         return redirect(reverse('index'))







from django.shortcuts import render, redirect, reverse
from django.contrib.auth.decorators import login_required
from .forms import UserProfileForm
from .models import UserCart, PaymentP
from django.db.models import Sum
from django.utils import timezone

@login_required
def spects_dashboard(request):
    if request.user.is_authenticated:
        user = request.user
        if user.role == 3 and not request.path == reverse('spects_dashboard'):
            return redirect(reverse('spects_dashboard'))
        else:
            form = UserProfileForm(instance=user.userprofile)

            if request.method == 'POST':
                form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
                if form.is_valid():
                    form.save()

            # Fetch total products sold today
            today = timezone.now().date()
            total_products_sold_today = UserCart.objects.filter(created_at__date=today).count()

            # Fetch total amount earned today
            total_amount_earned_today = PaymentP.objects.filter(timestamp__date=today).aggregate(total_amount=Sum('amount'))['total_amount']

            # Ensure to handle cases where total_amount_earned_today might be None
            total_amount_earned_today = total_amount_earned_today if total_amount_earned_today is not None else 0

            return render(request, 'spects_dashboard.html', {
                'total_products_sold_today': total_products_sold_today,
                'total_amount_earned_today': total_amount_earned_today,
                'form': form,  # Pass the form to the template for rendering
            })
    else:
        return redirect(reverse('index'))
















# from django.contrib.auth.decorators import login_required
# from django.shortcuts import render, redirect, reverse
# from .models import UserCart
# from django.db.models import Sum
# from datetime import datetime
# from .forms import UserProfileForm

# from django.db.models import F

# @login_required
# def spects_dashboard(request):
#     if request.user.is_authenticated:
#         user = request.user
#         if user.role == 3 and not request.path == reverse('spects_dashboard'):
#             return redirect(reverse('spects_dashboard'))
#         else:
#             # Calculate total frames sold today
#             today = datetime.now().date()
#             frames_sold_today = UserCart.objects.filter(created_at__date=today).aggregate(total_sold=Sum('quantity'))['total_sold'] or 0

#             # Calculate total amount generated today
#             total_amount_today = UserCart.objects.filter(created_at__date=today).aggregate(total_amount=Sum(F('frame__price') * F('quantity')))['total_amount'] or 0

#             # Calculate total frames sold this month
#             this_month = datetime.now().date().replace(day=1)
#             frames_sold_this_month = UserCart.objects.filter(created_at__date__gte=this_month).aggregate(total_sold=Sum('quantity'))['total_sold'] or 0

#             # Calculate total amount generated this month
#             total_amount_this_month = UserCart.objects.filter(created_at__date__gte=this_month).aggregate(total_amount=Sum(F('frame__price') * F('quantity')))['total_amount'] or 0

#             form = UserProfileForm(instance=user.userprofile)

#             if request.method == 'POST':
#                 form = UserProfileForm(request.POST, request.FILES, instance=user.userprofile)
#                 if form.is_valid():
#                     form.save()
#             context = {
#                 'user': user,
#                 'frames_sold_today': frames_sold_today,
#                 'total_amount_today': total_amount_today,
#                 'frames_sold_this_month': frames_sold_this_month,
#                 'total_amount_this_month': total_amount_this_month,
#                 'form': form
#             }
#             return render(request, 'spects_dashboard.html', context)
#     else:
#         return redirect(reverse('index'))








# views.py
from django.shortcuts import render, redirect
from .forms import FrameForm
from .models import Frame
@login_required
def add_product(request):
    if request.method == 'POST':
        form = FrameForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('spects_dashboard')  # Change 'dashboard' to your actual dashboard URL
    else:
        form = FrameForm()

    return render(request, 'spects/add_product.html', {'form': form})









# # views.py
# from django.shortcuts import render, get_object_or_404, redirect
# from .models import Frame
# from .forms import FrameForm

# def frame_list(request):
#     frames = Frame.objects.all()
#     return render(request, 'frame_list.html', {'frames': frames})

# def frame_detail(request, frame_id):
#     frame = get_object_or_404(Frame, frame_id=frame_id)
#     return render(request, 'frame_detail.html', {'frame': frame})

# def edit_frame(request, frame_id):
#     frame = get_object_or_404(Frame, frame_id=frame_id)

#     if request.method == 'POST':
#         form = FrameForm(request.POST, instance=frame)
#         if form.is_valid():
#             form.save()
#             return redirect('frame_list')
#     else:
#         form = FrameForm(instance=frame)

#     return render(request, 'edit_frame.html', {'form': form, 'frame': frame})

# def delete_frame(request, frame_id):
#     frame = get_object_or_404(Frame, frame_id=frame_id)

#     if request.method == 'POST':
#         frame.delete()
#         return redirect('frame_list')

#     return render(request, 'delete_frame.html', {'frame': frame})

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from .models import Frame
from .forms import FrameForm
@login_required
def frame_list(request):
    frames = Frame.objects.all()
    print(frames)  # Add this line to print frames in the console
    return render(request, 'frame_list.html', {'frames': frames})

@login_required
def frame_detail(request, frame_id):
    frame = get_object_or_404(Frame, frame_id=frame_id)
    return render(request, 'frame_detail.html', {'frame': frame})

@login_required
def edit_frame(request, frame_id):
    frame = get_object_or_404(Frame, frame_id=frame_id)

    if request.method == 'POST':
        form = FrameForm(request.POST, request.FILES, instance=frame)
        if form.is_valid():
            form.save()
            return redirect('frame_list')
    else:
        form = FrameForm(instance=frame)

    return render(request, 'frame_edit.html', {'form': form, 'frame': frame})

@login_required
def delete_frame(request, frame_id):
    frame = get_object_or_404(Frame, frame_id=frame_id)

    if request.method == 'POST':
        frame.delete()
        return redirect('frame_list')

    return render(request, 'frame_delete.html', {'frame': frame})







# views.py
from django.shortcuts import render
from .models import Frame

from django.db.models import F

@login_required
def eyeglasses(request):
    eyeglasses_frames = Frame.objects.filter(category='Eyeglasses')

    # Handle brand filtering
    selected_brands = request.GET.getlist('brand', [])
    if selected_brands:
        eyeglasses_frames = eyeglasses_frames.filter(brand_name__in=selected_brands)

    # Handle price sorting
    sort_by = request.GET.get('sort', None)
    if sort_by == 'price_low_to_high':
        eyeglasses_frames = eyeglasses_frames.order_by('price')
    elif sort_by == 'price_high_to_low':
        eyeglasses_frames = eyeglasses_frames.order_by('-price')

    # Handle gender filtering
    gender = request.GET.get('gender', None)
    if gender in ['M', 'F', 'K']:
        eyeglasses_frames = eyeglasses_frames.filter(gender=gender)

    context = {
        'eyeglasses_frames': eyeglasses_frames,
        'selected_brands': selected_brands,
        'BRAND_CHOICES': Frame.BRAND_CHOICES,
    }

    return render(request, 'eyeglasses/eyeglasses.html', context)


from django.db.models import F

@login_required
def sunglasses(request):
    sunglasses_frames = Frame.objects.filter(category='Sunglasses')

    # Handle brand filtering
    selected_brands = request.GET.getlist('brand', [])
    if selected_brands:
        sunglasses_frames = sunglasses_frames.filter(brand_name__in=selected_brands)

    # Handle price sorting
    sort_by = request.GET.get('sort', None)
    if sort_by == 'price_low_to_high':
        sunglasses_frames = sunglasses_frames.order_by('price')
    elif sort_by == 'price_high_to_low':
        sunglasses_frames = sunglasses_frames.order_by('-price')

    # Handle gender filtering
    gender = request.GET.get('gender', None)
    if gender in ['M', 'F', 'K']:
        sunglasses_frames = sunglasses_frames.filter(gender=gender)

    context = {
        'sunglasses_frames': sunglasses_frames,
        'selected_brands': selected_brands,
        'BRAND_CHOICES': Frame.BRAND_CHOICES,
    }

    return render(request, 'sunglasses/sunglasses.html', context)


from django.db.models import F

@login_required
def computerglasses(request):
    computerglasses_frames = Frame.objects.filter(category='Computer Glasses')

    # Handle brand filtering
    selected_brands = request.GET.getlist('brand', [])
    if selected_brands:
        computerglasses_frames = computerglasses_frames.filter(brand_name__in=selected_brands)

    # Handle price sorting
    sort_by = request.GET.get('sort', None)
    if sort_by == 'price_low_to_high':
        computerglasses_frames = computerglasses_frames.order_by('price')
    elif sort_by == 'price_high_to_low':
        computerglasses_frames = computerglasses_frames.order_by('-price')

    # Handle gender filtering
    gender = request.GET.get('gender', None)
    if gender in ['M', 'F', 'K']:
        computerglasses_frames = computerglasses_frames.filter(gender=gender)

    context = {
        'computerglasses_frames': computerglasses_frames,
        'selected_brands': selected_brands,
        'BRAND_CHOICES': Frame.BRAND_CHOICES,
    }

    return render(request, 'computerglasses/computerglasses.html', context)





from django.shortcuts import render, get_object_or_404

from .models import Frame

def frame_details_common_view(request, frame_id):
    frame = get_object_or_404(Frame, pk=frame_id)
    # You may need to retrieve random_frames for cross-promotion
    # Adjust the context as needed
    random_frames = Frame.objects.exclude(pk=frame_id).order_by('?')[:4]

    context = {
        'frame': frame,
        'random_frames': random_frames,
    }

    return render(request, 'frame_details_common.html', context)


#22/02


# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Frame

# def cart_view(request):
#     return render(request, 'cart.html')

# def add_to_cart(request, frame_id):
#     frame = get_object_or_404(Frame, pk=frame_id)

#     # Get or create the cart in session
#     cart = request.session.get('cart', {})

#     # Convert frame_id to string
#     frame_id_str = str(frame_id)

#     # Add frame to cart
#     if frame_id_str not in cart:
#         cart[frame_id_str] = {
#             'name': frame.name,
#             'brand_name': frame.brand_name,
#             'price': str(frame.price),
#             'quantity': 1,
#             'thumbnail': frame.thumbnail.url,
#         }
#     else:
#         # Update quantity if frame is already in cart
#         cart[frame_id_str]['quantity'] += 1

#     # Save cart in session
#     request.session['cart'] = cart

#     return redirect('cart')



# from django.http import JsonResponse

# def get_cart_data(request):
#     cart_json = request.session.get('cart', '{}')
#     cart = json.loads(cart_json) if cart_json else {}
    
#     cart_items = []
#     total_price = 0

#     for item in cart.values():
#         total_price += item['price'] * item['quantity']
#         cart_items.append({
#             'name': item['name'],
#             'quantity': item['quantity'],
#             'price': item['price'],
#             'thumbnail': item['thumbnail'],
#         })

#     cart_data = {
#         'items': cart_items,
#         'total_price': total_price,
#     }

#     return JsonResponse(cart_data)




# views.py 22/02

# def remove_from_cart(request, frame_id):
#     frame_id = str(frame_id)
#     if 'cart' in request.session and frame_id in request.session['cart']:
#         del request.session['cart'][frame_id]
#         request.session.modified = True

#     return redirect('cart')












from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

@login_required
def spects_edit_profile(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user.userprofile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('spects_edit_profile')
        else:
            messages.error(request, 'Error updating your profile. Please correct the errors below.')
    else:
        user_form = CustomUserForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user.userprofile)

    return render(request, 'spects_edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})




from django.contrib.auth.forms import PasswordChangeForm

@login_required
def spects_change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important to update the session
            messages.success(request, 'Your password was successfully updated!')
            return redirect('spects_change_password')
        else:
            messages.error(request, 'Error updating your password. Please correct the errors below.')
    else:
        form = PasswordChangeForm(request.user)

    return render(request, 'spects_change_password.html', {'form': form})



from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def spects_view_profile(request):
    if request.user.is_authenticated:
        user = request.user
        return render(request, 'spects_view_profile.html', {'user': user})
    else:
        # Redirect or handle the case when the user is not authenticated
        return redirect(reverse('spects_dashboard'))  # Assuming you have an 'index' URL pattern
    





# views.py Cart 28/02
# from django.shortcuts import render, redirect, get_object_or_404
# from .models import Frame, UserCart

# def add_to_cart(request, frame_id):
#     frame = get_object_or_404(Frame, pk=frame_id)
#     user = request.user

#     # Get or create the user cart
#     user_cart, created = UserCart.objects.get_or_create(user=user, frame=frame)

#     # If the cart already exists (not created), increment the quantity
#     if not created:
#         user_cart.quantity += 1
#         user_cart.save()

#     return redirect('cart')



# def view_cart(request):
#     user = request.user
#     user_cart_items = UserCart.objects.filter(user=user)
#     total_price = sum(item.total_price() for item in user_cart_items)

#     return render(request, 'cart.html', {'cart_items': user_cart_items, 'total_price': total_price})


# def remove_from_cart(request, frame_id):
#     user = request.user
#     frame = get_object_or_404(Frame, pk=frame_id)

#     # Get the user cart item
#     user_cart_item = get_object_or_404(UserCart, user=user, frame=frame)

#     # Decrement the quantity and remove if it becomes zero
#     user_cart_item.quantity -= 1
#     if user_cart_item.quantity <= 0:
#         user_cart_item.delete()
#     else:
#         user_cart_item.save()

#     return redirect('cart')
    

# views.py Add to cart Updated 29/02
# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Frame, UserCart
from django.contrib import messages

def add_to_cart(request, frame_id):
    frame = get_object_or_404(Frame, pk=frame_id)
    user = request.user

    # Get or create the user cart
    user_cart, created = UserCart.objects.get_or_create(user=user, frame=frame)

    # If the cart already exists (not created), increment the quantity
    if not created:
        user_cart.quantity += 1
        user_cart.save()

    return redirect('cart')

def view_cart(request):
    user = request.user
    user_cart_items = UserCart.objects.filter(user=user)
    total_price = sum(item.total_price() for item in user_cart_items)

    return render(request, 'cart.html', {'cart_items': user_cart_items, 'total_price': total_price})

def update_cart(request, frame_id):
    if request.method == 'POST':
        frame = get_object_or_404(Frame, pk=frame_id)
        user = request.user
        quantity = int(request.POST.get('quantity', 1))

        user_cart_item = get_object_or_404(UserCart, user=user, frame=frame)
        user_cart_item.quantity = quantity
        user_cart_item.save()

    return redirect('cart')

def remove_from_cart(request, frame_id):
    user = request.user
    frame = get_object_or_404(Frame, pk=frame_id)

    user_cart_item = get_object_or_404(UserCart, user=user, frame=frame)
    quantity_to_remove = user_cart_item.quantity

    user_cart_item.quantity -= quantity_to_remove
    if user_cart_item.quantity <= 0:
        user_cart_item.delete()
        messages.success(request, f"{frame.name} removed from the cart.")
    else:
        user_cart_item.save()

    return redirect('cart')









# views.py wishlist 29/02

from django.shortcuts import render, redirect, get_object_or_404
from .models import Wishlist, Frame

def view_wishlist(request):
    user = request.user
    wishlist_items = Wishlist.objects.filter(user=user)
    
    return render(request, 'wishlist.html', {'wishlist_items': wishlist_items})

def add_to_wishlist(request, frame_id):
    frame = get_object_or_404(Frame, pk=frame_id)
    user = request.user

    # Check if the frame is already in the wishlist
    if not Wishlist.objects.filter(user=user, frame=frame).exists():
        Wishlist.objects.create(user=user, frame=frame)

    return redirect('wishlist')

def remove_from_wishlist(request, frame_id):
    frame = get_object_or_404(Frame, pk=frame_id)
    user = request.user

    # Check if the frame is in the wishlist and remove it
    wishlist_item = Wishlist.objects.filter(user=user, frame=frame)
    if wishlist_item.exists():
        wishlist_item.delete()

    return redirect('wishlist')









from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Frame, UserCart, Order, OrderItem, ShippingAddress

def checkout(request):
    user = request.user
    user_cart_items = UserCart.objects.filter(user=user)
    total_price = sum(item.total_price() for item in user_cart_items)

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        address_line_1 = request.POST.get('address_line_1')
        address_line_2 = request.POST.get('address_line_2', '')  # Optional field
        city = request.POST.get('city')
        state = request.POST.get('state')
        pincode = request.POST.get('pincode')
        phone_number = request.POST.get('phone_number')

        # Optionally, you can perform validation checks here

        # Create a ShippingAddress instance
        shipping_address = ShippingAddress.objects.create(
            user=user,
            full_name=full_name,
            address_line_1=address_line_1,
            address_line_2=address_line_2,
            city=city,
            state=state,
            pincode=pincode,
            phone_number=phone_number,
            total_amount=total_price
        )

        # Redirect to the payment2 view with the shipping_address_id as a parameter
        return redirect(reverse('payment2', args=[shipping_address.id]))

    return render(request, 'checkout.html', {'cart_items': user_cart_items, 'total_price': total_price})

import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


razorpay_client = razorpay.Client(
     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))

def payment2(request, shipping_address_id):
    # Retrieve the shipping address using get_object_or_404 to ensure it exists
    shipping_address = get_object_or_404(ShippingAddress, id=shipping_address_id)
    t_fees = shipping_address.total_amount
    
    # For Razorpay integration
    currency = 'INR'
    amount = t_fees  # Get the total amount
    amount_in_paise = int(amount * 100)  # Convert to paise

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    # Extract the Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    
    # Define your callback URL here
    callback_url = reverse('paymenthandler2', args=[shipping_address_id])

    # Create a Payment object
    payment = PaymentP.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        payment_id="",
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        shippingAddress=shipping_address
    )

    # Prepare the context data
    context = {
        'user': request.user,
        'shipping_address': shipping_address,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
    }

    return render(request, 'shipping_details.html', context)


# @csrf_exempt
# def payment_confirmation(request, order_id):
#     try:
#         # Retrieve the appointment based on the order_id
from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from .models import PaymentP, CustomUser, ShippingAddress
from django.conf import settings
import razorpay
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import UserCart


razorpay_client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))





from django.core.serializers.json import DjangoJSONEncoder
import json
from django.db import transaction


@csrf_exempt
def paymenthandler2(request, shipping_address_id):
    if request.method == "POST":
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }

        result = razorpay_client.utility.verify_payment_signature(params_dict)

        try:
            payment = PaymentP.objects.get(razorpay_order_id=razorpay_order_id)
        except PaymentP.DoesNotExist:
            return HttpResponseBadRequest("Payment matching query does not exist.")

        amount = int(payment.amount * 100)

        razorpay_client.payment.capture(payment_id, amount)

        # Fetch cart items and serialize them
        user = request.user
        cart_items = UserCart.objects.filter(user=user)
        purchased_items = [{'frame_name': cart_item.frame.name, 'quantity': cart_item.quantity} for cart_item in cart_items]

        # Update the purchased_items field in the payment
        payment.purchased_items = json.dumps(purchased_items, cls=DjangoJSONEncoder)
        payment.payment_id = payment_id
        payment.payment_status = PaymentP.PaymentStatusChoices.SUCCESSFUL
        payment.save()

        # Retrieve the shipping address associated with the payment
        shipping_address = ShippingAddress.objects.get(pk=shipping_address_id)

        # Decrease stock quantity for each frame in the cart
        user = request.user
        cart_items = UserCart.objects.filter(user=user)
        with transaction.atomic():
            for cart_item in cart_items:
                frame = cart_item.frame
                if frame.stock_quantity >= cart_item.quantity:
                    frame.stock_quantity -= cart_item.quantity
                    frame.save()
                else:
                    # Handle the case where stock quantity is insufficient
                    return HttpResponseBadRequest("Insufficient stock quantity.")

        # Delete items from the cart after successful payment
        cart_items.delete()

        # Render email template with shipping address details
        
        email_subject = "Your Payment is Successful!"
        email_message_html = render_to_string('payment_success_email.html', {'shipping_address': shipping_address})
        email_message_text = strip_tags(email_message_html)  # Strip HTML tags for plain text version

        # Send email to the user
        send_mail(
            email_subject,
            email_message_text,  # Plain text version of the email
            'irisgloweyecare@gmail.com',  # Sender's email address
            [request.user.email],  # List of recipient email addresses
            html_message=email_message_html,  # HTML version of the email
            fail_silently=False,
        )

        return render(request, 'payment_confirmation_frame.html', {'shipping_address': shipping_address})

    else:
        return HttpResponseBadRequest("Invalid request method.")





# Modify the order_details view
import json

def order_details(request):
    user = request.user

    # Retrieve successful payments for the current user
    successful_payments = PaymentP.objects.filter(user=user, payment_status='successful')

    purchased_items = []
    for payment in successful_payments:
        if payment.purchased_items:
            purchased_items.extend(json.loads(payment.purchased_items))

    context = {
        'purchased_items': purchased_items,
    }

    return render(request, 'order_details.html', context)