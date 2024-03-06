import datetime
import io
from itertools import zip_longest
import time
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from django.urls import reverse
from IrisGlowApp.forms import UserProfileForm
from IrisGlowApp.models import CustomUser,UserProfile
from .forms import AppointmentForm, CurrentUserForm, CustomUserForm, DoctorProfileForm
from .models import Appointments, Doctor, Payment


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



@login_required
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

@login_required
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



@login_required
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












# appointment views.py
from .models import Appointments, DoctorDayOff
from .forms import AppointmentForm, CurrentUserForm
from .models import CustomUser
from datetime import time
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from datetime import datetime



def appointment(request, t_id):
    therapist = get_object_or_404(CustomUser, id=t_id)
    context = None

    if request.method == 'POST':
        date_str = request.POST.get('date')
        time_str = request.POST.get('time_slot')

        # Use datetime.strptime from the correct module
        date = datetime.strptime(date_str, '%Y-%m-%d').date()

        # Parse the date and time strings to datetime.date and datetime.time objects
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
        time_parts = time_str.split(':')
        time_slot = time(int(time_parts[0]), int(time_parts[1]))

        
        # Check if the selected date is a day when the therapist has taken a day off
        if DoctorDayOff.objects.filter(doctor=therapist, date=date).exists():
            messages.error(request, 'The therapist is on leave on the selected date. Please choose a different date.')
            return redirect('appointment', t_id=t_id)

        # Rest of your view code...
        existing_appointment = Appointments.objects.filter(client=request.user, date=date, time_slot=time_slot).first()

        if existing_appointment:
            context = {
                'error': 'You have already scheduled an appointment for the selected Date and Time Slot',
                'therapist': therapist,
            }
        elif Appointments.objects.filter(client=request.user, date=date).exists():
            context = {
                'error': 'You have already scheduled an appointment for the selected Date.',
                'therapist': therapist,
            }
        else:
            is_time_slot_available = is_time_slot_available_for_doctor(therapist, date, time_slot)
            if is_time_slot_available:
                form = AppointmentForm(request.POST)
                form.instance.client = request.user
                form.instance.therapist = therapist

                if form.is_valid():
                    # appointment = form.save()
                    appointment1 = form.save()
                    appointment_fee=300
                    if appointment1.id is not None:
                        return redirect('payment', appointment_id=appointment1.id, t_fees=appointment_fee)
                    else:
        # Handle the case where the appointment instance is not saved
                        print('Failed to save the appointment. Please try again.')
                    # return redirect('appointment_confirmation', appointment_id=appointment.id)
                # return redirect('payment',appointment_id=appointment1.id,t_fees=appointment_fee)
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

# Rest of your views...

def is_time_slot_available_for_doctor(therapist, date, time_slot):
    # Convert the selected time slot to a timezone-aware datetime object
    selected_time = timezone.datetime.combine(date, time_slot)
    
    # Check if the time slot is available for the specific doctor and date
    existing_appointment = Appointments.objects.filter(therapist=therapist, date=date, time_slot=selected_time).first()
    return existing_appointment is None

# Rest of your views...

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
















#appointment confirmationpage
from django.shortcuts import render

def appointment_confirmation(request, appointment_id):
    appointment = get_object_or_404(Appointments, id=appointment_id)
    context = {
        'appointment': appointment,
    }
    return render(request, 'appointment_confirmation.html', context)







def view_appointments(request):
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

    return render(request, 'doctor/view_appointments.html', context)








#view doctors by admin
from django.shortcuts import render
from .models import CustomUser
@login_required
def doctor_list(request):
    doctors = CustomUser.objects.filter(doctor=True)
    return render(request, 'doctor_list.html', {'doctors': doctors})





from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from .models import Doctor
@login_required
def search_doctor(request):
    query = request.GET.get('query')
    speciality = request.GET.get('speciality')
    experience = request.GET.get('experience')

    # Use Q objects to filter doctors based on first name, last name, or speciality name
    doctors = Doctor.objects.filter(
        Q(user__first_name__icontains=query) |
        Q(user__last_name__icontains=query)
    )

    if speciality:
        doctors = doctors.filter(speciality_name__speciality_name__icontains=speciality)

    if experience:
        doctors = doctors.filter(experience__gte=experience)

    # Create a list of dictionaries containing doctor information
    doctors_data = [
        {
            'id': doctor.user.id,
            'first_name': doctor.user.first_name,
            'last_name': doctor.user.last_name,
            'speciality_name': doctor.speciality_name.speciality_name,
            'profile_picture': doctor.user.userprofile.profile_picture.url,
            'qualification': doctor.qualification,
            'experience': doctor.experience,
        }
        for doctor in doctors
    ]

    return JsonResponse({'doctors': doctors_data})


@login_required
def doctor_search(request):
    return render(request, 'doctor_search.html')














#payment



import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest


razorpay_client = razorpay.Client(
     auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))



def payment(request, appointment_id,t_fees):
    # Use get_object_or_404 to get the Subscription object based on sub_id
        # Retrieve subscription features from a specific Subscription instance
    # You may want to retrieve a specific subscription
    print(t_fees)
    t_fees = float(request.resolver_match.kwargs['t_fees'])
    print(t_fees)

    appointments = Appointments.objects.all()
    current_appointment = Appointments.objects.get(pk=appointment_id)
    # For Razorpay integration
    currency = 'INR'
    amount = t_fees  # Get the subscription price
    amount_in_paise = int(amount * 100)  # Convert to paise
    print(amount_in_paise)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = reverse('paymenthandler', args=[appointment_id])  # Define your callback URL here

    phone=current_appointment.client.phone
    print(phone)
    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        payment_id="",
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        appointment=current_appointment
    )
    appointment=current_appointment
    # Prepare the context data
    context = {
        'user': request.user,
        'appointment':appointment,
        # 'therapy_fee':t_fees,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
        'phone':phone,
        
    }

    return render(request, 'client/razorpay_payment.html', context)


# @csrf_exempt
# def payment_confirmation(request, order_id):
#     try:
#         # Retrieve the appointment based on the order_id
@csrf_exempt
def paymenthandler(request, appointment_id):
    # Only accept POST requests.
    if request.method == "POST":
        # Get the required parameters from the POST request.
        payment_id = request.POST.get('razorpay_payment_id', '')
        razorpay_order_id = request.POST.get('razorpay_order_id', '')
        signature = request.POST.get('razorpay_signature', '')
        params_dict = {
            'razorpay_order_id': razorpay_order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        }
    # Verify the payment signature.
        result = razorpay_client.utility.verify_payment_signature(params_dict)

        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)
        amount = int(payment.amount * 100)  # Convert Decimal to paise

        # Capture the payment.
        razorpay_client.payment.capture(payment_id, amount)
        payment = Payment.objects.get(razorpay_order_id=razorpay_order_id)

        # Update the order with payment ID and change status to "Successful."
        payment.payment_id = payment_id
        payment.payment_status = Payment.PaymentStatusChoices.SUCCESSFUL
        payment.save()

        try:
            update_appointment = Appointments.objects.get(id=appointment_id)
            print(update_appointment)
            update_appointment.status = 'pending'
            update_appointment.save()
            pay_amt= payment.amount
            payee = update_appointment.client.first_name
            email = update_appointment.client.email
            ap_date=update_appointment.date
            ap_time=update_appointment.time_slot
            therapist = update_appointment.therapist.first_name
            appointment_email(email,  payee, ap_date, ap_time, pay_amt,therapist,payment)
        except Appointments.DoesNotExist:
            # Handle the case where the appointment with the given ID does not exist
            return HttpResponseBadRequest("Invalid appointment ID")
       
        # Render the success page on successful capture of payment.
        return render(request, 'payment_confirmation.html',{'appointment':update_appointment})

    else:
        update_appointment = Appointments.objects.get(id=appointment_id)
        update_appointment.payment_status = False
        update_appointment.save()

        # If other than POST request is made.
        return HttpResponseBadRequest()




from django.core.files.base import File

from django.core.mail import EmailMessage

def appointment_email(email, payee, ap_date, ap_time, therapist, payment, pay_amt):
    subject = "Appointment Confirmation"

    formatted_time = ap_time.strftime('%I:%M %p')
    formatted_date = ap_date.strftime('%B %d, %Y')

    message = f"Dear {payee},\n\nWe are pleased to confirm your upcoming appointment with our doctor, {therapist}, scheduled for {formatted_date} at {formatted_time}.\n\nYour payment receipt is attached to this email for your reference.\n\nThank you for choosing our services. We look forward to providing you with the best care possible.\n\nBest regards,\nIrisGlow Team"
    from_email = 'irisgloweyecare@gmail.com'
    recipient_list = [email]

    # Generate the PDF content
    pdf_content = generate_pdf_invoice(payee, pay_amt, payment)

    # Create a file-like object using Django's File class
    pdf_file = File(io.BytesIO(pdf_content), name=f"{payee}_invoice.pdf")

    # Attach the file to the email
    email_message = EmailMessage(subject, message, from_email, recipient_list)
    email_message.attach(pdf_file.name, pdf_content, 'application/pdf')  # Use pdf_content instead of pdf_file.read()
    email_message.send()





from django.template.loader import get_template
from django.http import HttpResponse
import io
from xhtml2pdf import pisa
   

# views.py
from django.template.loader import get_template
from django.http import HttpResponse
import io
from xhtml2pdf import pisa

def generate_pdf_invoice(payee, pay_amt, payment):
    template_path = "invoice.html"
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{payee}_invoice.pdf"'

    template = get_template(template_path)
    context = {
        'payee': payee,
        'amount': pay_amt,
        'payment': payment,  # Pass the payment object to the template
    }
    html = template.render(context)

    pdf_buffer = io.BytesIO()
    pisa.pisaDocument(io.BytesIO(html.encode("UTF-8")), pdf_buffer)

    pdf_content = pdf_buffer.getvalue()
    pdf_buffer.close()

    return pdf_content







def payment(request, appointment_id,t_fees):
    # Use get_object_or_404 to get the Subscription object based on sub_id
        # Retrieve subscription features from a specific Subscription instance
    # You may want to retrieve a specific subscription
    print(t_fees)
    t_fees = float(request.resolver_match.kwargs['t_fees'])
    print(t_fees)

    appointment = Appointments.objects.all()
    current_appointment = Appointments.objects.get(pk=appointment_id)
    # For Razorpay integration
    currency = 'INR'
    amount = t_fees  # Get the subscription price
    amount_in_paise = int(amount * 100)  # Convert to paise
    print(amount_in_paise)

    # Create a Razorpay Order
    razorpay_order = razorpay_client.order.create(dict(
        amount=amount_in_paise,
        currency=currency,
        payment_capture='0'
    ))

    # Order ID of the newly created order
    razorpay_order_id = razorpay_order['id']
    callback_url = reverse('paymenthandler', args=[appointment_id])  # Define your callback URL here
    phone=current_appointment.client.phone
    print(phone)
    payment = Payment.objects.create(
        user=request.user,
        razorpay_order_id=razorpay_order_id,
        payment_id="",
        amount=amount,
        currency=currency,
        payment_status=Payment.PaymentStatusChoices.PENDING,
        appointment=current_appointment
    )
    appointment=current_appointment
    # Prepare the context data
    context = {
        'user': request.user,
        'appointment':appointment,
        # 'therapy_fee':t_fees,
        'razorpay_order_id': razorpay_order_id,
        'razorpay_merchant_key': settings.RAZOR_KEY_ID,
        'razorpay_amount': amount_in_paise,
        'currency': currency,
        'amount': amount_in_paise / 100,
        'callback_url': callback_url,
        'phone':phone,
        
    }

    return render(request, 'razorpay_payment.html', context)
































# views.py
from django.shortcuts import render, redirect
from .forms import DoctorDayOffForm
from .models import DoctorDayOff
from django.contrib import messages

@login_required
def doctor_day_off(request):
    if request.method == 'POST':
        form = DoctorDayOffForm(request.POST)
        if form.is_valid():
            doctor_day_off = form.save(commit=False)
            doctor_day_off.doctor = request.user
            doctor_day_off.save()
            messages.success(request, 'Day off added successfully.')
            return redirect('doctor_day_off_confirmation')
        else:
            messages.error(request, 'Invalid form submission. Please check the form data.')
    else:
        form = DoctorDayOffForm()

    context = {'form': form}
    return render(request, 'doctor/doctor_day_off.html', context)



@login_required
def doctor_day_off_confirmation(request):
    return render(request, 'doctor/doctor_day_off_confirmation.html')


@login_required
def doctordashboard(request):
    return render(request,'doctordashboard.html',)