from itertools import zip_longest
import time
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from IrisGlowApp.forms import UserProfileForm
from IrisGlowApp.models import CustomUser,UserProfile
from .forms import AppointmentForm, CurrentUserForm, CustomUserForm, DoctorProfileForm
from .models import Appointments, Doctor


User = get_user_model()


# Create your views here.
@login_required
def addDoctor(request):
    if request.method == 'POST':
        user_form = CustomUserForm(request.POST)

        Specialization = request.POST.get('Specialization', None)
        License = request.POST.get('License', None)

        print(Specialization)
        print(License)
        
        

        if user_form.is_valid():
            email = user_form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                msg = 'Email already exists. Please use a different email address.'
            else:
                user = user_form.save(commit=False)
                password = user_form.cleaned_data['password']

            # Send welcome email
                send_welcome_email(user.email, password, user.first_name, user.last_name)

                user.set_password(password)
                user.is_active = True

                user.role = CustomUser.DOCTOR  # Set the role to "Doctor"
                user.save()

            # Check if the user has the role=2 (Doctor)
                if user.role == CustomUser.DOCTOR:
                    doctor = Doctor(user=user)  # Create a Doctor instance
                    doctor.qualification=Specialization
                    doctor.license=License
                    doctor.save()

                user_profile = UserProfile(user=user)
            
                user_profile.save()

                return redirect('admindashboard')

    else:
        user_form = CustomUserForm()

    context = {
        'user_form': user_form
    }

    return render(request, 'admin/adddoctor.html', context)




def send_welcome_email(email, password, first_name, last_name):

    login_url = 'http://127.0.0.1:8000/accounts/login/'  # Update with your actual login URL
    login_button = f'Click here to log in: {login_url}'


    subject = 'IrisGlow - Doctor Registration'
    message = f"Hello {first_name} {last_name},\n\n"
    message += f"Welcome to IrisGlow, your platform for holistic wellness and healing. We are thrilled to have you on board as a part of our dedicated team of therapists.\n\n"
    message += f"Your registration is complete, and we're excited to have you join us. Here are your login credentials:\n\n"
    message += f"Email: {email}\nPassword: {password}\n\n"
    message += "Please take a moment to log in to your account using the provided credentials. Once you've logged in, we encourage you to reset your password to something more secure and memorable.\n\n"
    message += login_button
    message += "\n\nIrisGlow is committed to providing a safe and supportive environment for both therapists and clients. Together, we can make a positive impact on the lives of those seeking healing and guidance.\n"
    message += "Thank you for joining the IrisGlow community. We look forward to your contributions and the positive energy you'll bring to our platform.\n\n"
    message += "Warm regards,\nThe IrisGlow Team\n\n"
    


    from_email='akkushaji1511@gmail.com'
      # Replace with your actual email
    recipient_list = [email]
    
    send_mail(subject, message, from_email, recipient_list)



#02/11


from django.core.paginator import Paginator

def doctor(request):
    therapists = Doctor.objects.all()
    cuser = CustomUser.objects.filter(role=CustomUser.DOCTOR, id__in=therapists.values_list('user_id', flat=True))
    uprofile = UserProfile.objects.filter(user_id__in=cuser.values_list('id', flat=True))
    combined_data = list(zip_longest(cuser, uprofile, therapists))

    # Create a Paginator object with a specified number of therapists per page
    paginator = Paginator(combined_data, per_page=4)  # Change '10' to the number of therapists per page you prefer

    # Get the current page number from the request's GET parameters
    page_number = request.GET.get('page')

    # Retrieve the therapists for the current page
    therapists_page = paginator.get_page(page_number)                   
    return render(request, 'team.html' , {'therapists_page': therapists_page})



@login_required
def viewdoctor(request, user_id):
    users = get_object_or_404(CustomUser, id=user_id)
    print(users.first_name)
    therapist = Doctor.objects.get(user=users)
    profile = UserProfile.objects.get(user=users)

    context={
        'users' : users,
        'userprofile' : profile,
        'therapist' : therapist
        }
    return render(request, 'teams/doctor1.html', context)




def doctor_dashboard(request):
     return render(request,'doctor_dashboard.html',)


@login_required
def doctorprofile(request):
    
    user = request.user

    # Initialize variables for user profile and therapist info
    user_profile = None
 
    if user.userprofile.user.role == 2:
        try:
            # Get the user profile information
            user_profile = UserProfile.objects.get(user=user.userprofile.user)
           
        except UserProfile.DoesNotExist:
            user_profile = None
            

    context = {
        'user': user,
        'user_profile': user_profile,  # User profile information
    }

    
@login_required
def doctorprofile(request):
    
    # Retrieve the logged-in user's information
    user = request.user

    # Initialize variables for user profile and therapist info
    user_profile = None
    therapist_info = None
    if user.userprofile.user.role == 1:
        return redirect("profile")
    # Check if the user has a therapist role (role == 2)
    elif user.userprofile.user.role == 2:
        try:
            # Get the user profile information
            user_profile = UserProfile.objects.get(user=user.userprofile.user)
            # Get the therapist's specific information
            therapist = Doctor.objects.get(user=user.userprofile.user)

            # Include all fields from the Therapist model in therapist_info
            therapist_info = {
                'bio': therapist.bio,
                'qualification': therapist.qualification,
                'license': therapist.license,
                'experience': therapist.experience,
                'speciality_name': therapist.speciality_name,
            }
        except UserProfile.DoesNotExist or Doctor.DoesNotExist:
            user_profile = None
            therapist_info = None

    context = {
        'user': user,
        'user_profile': user_profile,  # User profile information
        'therapist_info': therapist_info,  # Therapist-specific information
    }

    return render(request, 'doctor/view_doctor_profile.html', context)




@login_required
def editdoctorprofile(request):
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

    


@login_required
def editdoctorprofile(request):
    user_id = request.user.id
    user = CustomUser.objects.get(id=user_id)
    therapist = Doctor.objects.get(user=user)
    user_profile = UserProfile.objects.get(user=user)

    if request.method == 'POST':
        user_form = CustomUserForm(request.POST, instance=user)
        therapist_form = DoctorProfileForm(request.POST, instance=therapist)
        user_profile_form = UserProfileForm(request.POST, request.FILES, instance=user_profile)

        if user_form.is_valid() and therapist_form.is_valid() and user_profile_form.is_valid():
            user_form.save()
            therapist_form.save()
            user_profile_form.save()
            return redirect('doctorprofile')  # Redirect to the user's profile page after editing

    else:
        user_form = CustomUserForm(instance=user)
        therapist_form = DoctorProfileForm(instance=therapist)
        user_profile_form = UserProfileForm(instance=user_profile)
    context = {
        'user_form': user_form,
        'therapist_form': therapist_form,
        'user_profile_form': user_profile_form,
        'user_profile':user_profile
    }

    return render(request, 'doctor/edit_doctor_profile.html', context)




# #Appointment

# from django.shortcuts import render, redirect
# from .models import Appointments
# from .forms import AppointmentForm,CurrentUserForm

# @login_required
# def appointment(request, t_id):
#     therapist = get_object_or_404(CustomUser, id=t_id)
#     context = None

#     if request.method == 'POST':
#         date = request.POST.get('date')
#         time_slot = request.POST.get('time_slot')

#         # Check if the current user (client) has already booked an appointment for the same date and time slot
#         existing_appointment = Appointments.objects.filter(client=request.user, date=date, time_slot=time_slot).first()

#         # Check if the current user (client) has already booked an appointment for the same date
#         existing_appointment_same_date = Appointments.objects.filter(client=request.user, date=date).first()

#         if existing_appointment:
#             apps = Appointments.objects.filter(date=date, time_slot=time_slot)
#             time_slots = {time(9, 0): 1, time(11, 0): 1, time(13, 0): 1, time(15, 0): 1, time(17, 0): 1}
#             for app in apps:
#                 time_slots[app.time_slot] = 0

#             available_slots = [time_slot.strftime('%I:%M %p') for time_slot, available in time_slots.items() if available]
#             available_slots = ", ".join(available_slots)
#             print(available_slots)

#             user = request.user
#             initial_data = {
#                 'client': user,
#                 'client_name': user.first_name,
#                 'client_phone': user.phone,
#                 'therapist': therapist.id,
#                 'therapist_name': therapist.first_name,
#             }
#             appointment_form = AppointmentForm(initial=initial_data)
#             user_form = CurrentUserForm(instance=user)
#             context = {
#                 'error': 'You have already scheduled an appointment for the selected Date and Time Slot',
#                 'therapist': therapist,
#                 'appointment_form': appointment_form,
#                 'user_form': user_form,
#                 'available_slots': available_slots
#             }
#         elif existing_appointment_same_date:
#             user = request.user
#             initial_data = {
#                 'client': user,
#                 'client_name': user.first_name,
#                 'client_phone': user.phone,
#                 'therapist': therapist.id,
#                 'therapist_name': therapist.first_name,
#             }
#             appointment_form = AppointmentForm(initial=initial_data)
#             user_form = CurrentUserForm(instance=user)
#             context = {
#                 'error': 'You have already scheduled an appointment for the selected Date',
#                 'therapist': therapist,
#                 'appointment_form': appointment_form,
#                 'user_form': user_form,
#             }
#         else:
#             form = AppointmentForm(request.POST)
#             form.instance.client = request.user
#             form.instance.therapist = therapist

#             if form.is_valid():
#                 form.save()
#                 return redirect('index')              

#     else:
#         user = request.user
#         initial_data = {
#             'client': user,
#             'client_name': user.first_name,
#             'client_phone': user.phone,
#             'therapist': therapist.id,
#             'therapist_name': therapist.first_name,
#         }
#         appointment_form = AppointmentForm(initial=initial_data)
#         user_form = CurrentUserForm(instance=user)
#         context = {'appointment_form': appointment_form, 'user_form': user_form, 'therapist': therapist}

#     return render(request, 'appointment.html', context)

# def get_available_time_slots(request):
#     therapist_id = request.GET.get('therapist_id')
#     therapist = get_object_or_404(CustomUser, id=therapist_id)
#     date = request.GET.get('date')

#     # Fetch existing appointments for the selected date and therapist
#     existing_appointments = Appointments.objects.filter(therapist=therapist, date=date)

#     # Create a list of all available time slots
#     all_time_slots = [time(9, 0), time(11, 0), time(13, 0), time(15, 0), time(17, 0)]

#     # Initialize a dictionary to store the availability of time slots
#     time_slot_availability = {time_slot: True for time_slot in all_time_slots}

#     # Mark time slots as unavailable if they are already booked
#     for appointment in existing_appointments:
#         if appointment.time_slot in time_slot_availability:
#             time_slot_availability[appointment.time_slot] = False

#     # Filter the available time slots
#     available_time_slots = [time_slot.strftime('%I:%M %p') for time_slot, is_available in time_slot_availability.items() if is_available]

#     return JsonResponse({'available_time_slots': available_time_slots})




from django.shortcuts import render, redirect
from django.http import JsonResponse
from .models import Appointments
from .forms import AppointmentForm, CurrentUserForm
from .models import CustomUser
from datetime import time
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required

@login_required
def appointment(request, t_id):
    therapist = get_object_or_404(CustomUser, id=t_id)
    context = None

    if request.method == 'POST':
        date = request.POST.get('date')
        time_slot = request.POST.get('time_slot')

        # Check if the current user (client) has already booked an appointment for the same date and time slot
        existing_appointment = Appointments.objects.filter(client=request.user, date=date, time_slot=time_slot).first()

        if existing_appointment:
            context = {
                'error': 'You have already scheduled an appointment for the selected Date and Time Slot',
                'therapist': therapist,
            }
        else:
            # Check if the selected time slot is available
            is_time_slot_available = is_time_slot_available_for_doctor(therapist, date, time_slot)
            if is_time_slot_available:
                form = AppointmentForm(request.POST)
                form.instance.client = request.user
                form.instance.therapist = therapist

                if form.is_valid():
                    form.save()
                    return redirect('index')
            else:
                context = {
                    'error': 'The selected time slot is not available. Please choose a different time slot.',
                    'therapist': therapist,
                }

    else:
        user = request.user
        initial_data = {
            'client': user,
            'client_name': user.first_name,
            'client_phone': user.phone,
            'therapist': therapist.id,
            'therapist_name': therapist.first_name,
        }
        appointment_form = AppointmentForm(initial=initial_data)
        user_form = CurrentUserForm(instance=user)
        context = {'appointment_form': appointment_form, 'user_form': user_form, 'therapist': therapist}

    return render(request, 'appointment.html', context)

def is_time_slot_available_for_doctor(therapist, date, time_slot):
    # Check if the time slot is available for the specific doctor and date
    existing_appointment = Appointments.objects.filter(therapist=therapist, date=date, time_slot=time_slot).first()
    return existing_appointment is None

def get_available_time_slots(request):
    therapist_id = request.GET.get('therapist_id')
    therapist = get_object_or_404(CustomUser, id=therapist_id)
    date = request.GET.get('date')

    # Fetch existing appointments for the selected date and therapist
    existing_appointments = Appointments.objects.filter(therapist=therapist, date=date)

    # Create a list of all available time slots
    all_time_slots = [time(9, 0), time(11, 0), time(13, 0), time(15, 0), time(17, 0)]

    # Initialize a dictionary to store the availability of time slots
    time_slot_availability = {time_slot: True for time_slot in all_time_slots}

    # Mark time slots as unavailable if they are already booked
    for appointment in existing_appointments:
        if appointment.time_slot in time_slot_availability:
            time_slot_availability[appointment.time_slot] = False

    # Filter the available time slots
    available_time_slots = [time_slot.strftime('%I:%M %p') for time_slot, is_available in time_slot_availability.items() if is_available]

    return JsonResponse({'available_time_slots': available_time_slots})








#view appointments

from django.shortcuts import render
from .models import Appointments

def view_appointments(request):
    # Assuming you have a way to identify the currently logged-in doctor
    doctor = request.user  # Replace this with your own logic to get the doctor

    # Fetch the doctor's appointments
    appointments = Appointments.objects.filter(therapist=doctor)

    context = {
        'doctor': doctor,
        'appointments': appointments,
    }

    return render(request, 'doctor/view_appointments.html', context)


