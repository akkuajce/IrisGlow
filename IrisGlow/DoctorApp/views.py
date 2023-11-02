from itertools import zip_longest
from django.shortcuts import get_object_or_404, render, redirect
from django.core.mail import EmailMessage
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model
from IrisGlowApp.models import CustomUser,UserProfile
from .forms import CustomUserForm
from .models import Doctor





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