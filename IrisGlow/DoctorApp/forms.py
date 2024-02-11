from django import forms
from django.contrib.auth import get_user_model


CustomUser = get_user_model()

class CustomUserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id':'pass',
        "class": "form-control form-control-lg",
        'placeholder': 'Enter Password'
    }))
    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'id':'cpass',
        "class": "form-control form-control-lg",
        'placeholder': 'Confirm Password'
    }))
    
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name','email','phone']
        widgets = {
            'first_name': forms.TextInput(attrs={
                "class": "form-control form-control-lg ",
                'placeholder': 'Enter Name',
                'id':'name'
            }),

             'last_name': forms.TextInput(attrs={
                "class": "form-control form-control-lg ",
                'placeholder': 'Enter Name',
                'id':'name'
            }),

            'email': forms.EmailInput(attrs={
                'id':'email',
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Email'
            }),
            'phone': forms.TextInput(attrs={
                'id':'phone',
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Phone Number'
            }),
            # 'role': forms.Select(attrs={
            #     "class": "form-control form-control-lg"
            # }),

        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')

    def save(self, commit=True):
        user = super().save(commit=False)
        password = self.cleaned_data["password"]
        user.set_password(password)
        
        if commit:
            user.save()
        return user
    


    # doctorapp/forms.py

from django import forms
from .models import Doctor

class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['qualification', 'license', 'experience', 'bio', 'speciality_name']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 4}),
            # Add more widgets for other fields if needed
        }









from django import forms
from datetime import date
from .models import Appointments
from IrisGlowApp.models import CustomUser

class BootstrapTextInput(forms.TextInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg bg-white"
        super().__init__(*args, **kwargs)

# Define a custom widget class with Bootstrap styling for select fields
class BootstrapSelect(forms.Select):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg bg-white"
        super().__init__(*args, **kwargs)

class BootstrapDateInput(forms.DateInput):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg datepicker"
        super().__init__(*args, **kwargs)

class AppointmentForm(forms.ModelForm):
    date = forms.DateField(
        widget=forms.DateInput(
            attrs={
                'placeholder': 'YYYY-MM-DD',
                'id': 'date',
                'name': 'date',
                'class': 'form-control form-control-lg',
                'type': 'date',
                'min': date.today().strftime('%Y-%m-%d')  # Set the minimum date to today
            }
        )
    )

    therapist_name = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter Doctor Name', 'id': '', 'class': 'form-control form-control-lg bg-white', 'disabled': 'disabled'}),
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Appointments
        fields = ['therapist_name', 'date', 'time_slot']
        widgets = {
            'time_slot': forms.Select(attrs={'placeholder': 'Select State', 'id': 'time_slot'}),
        }

class CurrentUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'email', 'phone']
        widgets = {
            'first_name': BootstrapTextInput(attrs={'placeholder': 'Enter Your Name', 'id': 'first_name', 'disabled': 'disabled'}),
            'email': BootstrapTextInput(attrs={'placeholder': 'Enter Your Email', 'id': 'email', 'disabled': 'disabled'}),
            'phone': BootstrapTextInput(attrs={'placeholder': 'Enter Your Phone', 'id': 'phone'}),
        }




















# forms.py
from django import forms
from .models import DoctorDayOff

class DoctorDayOffForm(forms.ModelForm):
    class Meta:
        model = DoctorDayOff
        fields = ['date']
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }






