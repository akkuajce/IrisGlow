from django import forms

from DoctorApp.models import Specialities
from .models import CustomUser, UserProfile

from datetime import date, timedelta

from django import forms

class BootstrapTextInput(forms.TextInput):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg bg-white"
        super().init(*args, **kwargs)

# Define a custom widget class with Bootstrap styling for select fields
class BootstrapSelect(forms.Select):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg bg-white"
        super().init(*args, **kwargs)


class BootstrapDateInput(forms.DateInput):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg datepicker"
        super().init(*args, **kwargs)





class BootstrapTextarea(forms.Textarea):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "form-control form-control-lg"
        kwargs["attrs"]["rows"] = 16  # Customize the number of rows as needed
        super().init(*args, **kwargs)

class BootstrapFileInput(forms.ClearableFileInput):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "custom-file-input"
        super().init(*args, **kwargs)

class BootstrapImageInput(forms.ClearableFileInput):
    def init(self, *args, **kwargs):
        kwargs.setdefault("attrs", {})
        kwargs["attrs"]["class"] = "custom-file-input"
        super().init(*args, **kwargs)

class CustomUserForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name','last_name', 'email', 'phone']
        widgets = {
            'first_name': BootstrapTextInput(attrs={'placeholder': 'Enter Your First Name', 'id': 'first_name'}),
            'last_name': BootstrapTextInput(attrs={'placeholder': 'Enter Your Last Name', 'id': 'last_name'}),
            'email': BootstrapTextInput(attrs={'placeholder': 'Enter Your Email', 'id': 'email'}),
            'phone': BootstrapTextInput(attrs={'placeholder': 'Enter Your Phone', 'id': 'phone'}),
        }

class UserProfileForm(forms.ModelForm):
    dob = forms.DateField(
        widget=BootstrapDateInput(attrs={'placeholder': 'YYYY-MM-DD', 'id': 'dobclient','type': 'date'})
    )

    profile_picture = forms.ImageField(
        widget=BootstrapImageInput(attrs={'id': 'pictureInput'})
    )
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'address','addressline1', 'addressline2','country', 'state', 'city', 'pin_code', 'gender', 'dob']
        widgets = {
             'profile_picture': BootstrapFileInput(attrs={'placeholder': 'Upload Profile Picture'}),
             'profile_picture': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
            'address': BootstrapTextInput(attrs={'placeholder': 'Address Line 1', 'id': 'address'}),
            'addressline1': BootstrapTextInput(attrs={'placeholder': 'Address Line 2', 'id': 'address1'}),
            'addressline2': BootstrapTextInput(attrs={'placeholder': 'Address Line 3', 'id': 'address2'}),
            'country': BootstrapSelect(attrs={'placeholder': 'Select Country', 'id': 'country'}),
            'state': BootstrapSelect(attrs={'placeholder': 'Select State', 'id': 'state'}),
            'city': BootstrapTextInput(attrs={'placeholder': 'Enter City', 'id': 'city'}),
            'pin_code': BootstrapTextInput(attrs={'placeholder': 'Enter Pin Code', 'id': 'zipcode'}),
            'gender': BootstrapSelect(attrs={'placeholder': 'Select Gender', 'id': 'gender'}),
            #'dob': forms.DateInput(attrs={'placeholder': 'Select Date of Birth', 'id': 'dob'}),
        }





from DoctorApp.models import Specialities
# from .validators import allow_only_images_validator

class SpecialityForm(forms.ModelForm):
    
    speciality_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                "class": "form-control form-control-lg",
                'placeholder': 'Enter Therapy Name',
                'id':'tname',
            }
        )
    )
    

    symptoms = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':'4',
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter Breif Description',
                'id':'therapyDescription'
                }
            )
        )
    
    diagnosis = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':'4',
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter Breif Description',
                'id':'therapyDescription'
                }
            )
        )

    treatments = forms.CharField(
        widget=forms.Textarea(
            attrs={
                'rows':'3',
                'class': 'form-control form-control-lg',
                'placeholder': 'Enter the benefits','id':'benefits',
                }
            )
        )

    class Meta:
        model = Specialities
        fields = ['speciality_name','symptoms', 'diagnosis','treatments']





 # forms.py Add Spects 09/02

from django import forms
from .models import CustomUser
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

class SpectsUserForm(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput(), label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'password', 'confirm_password']
        widgets = {
            'password': forms.PasswordInput(),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise ValidationError(_('Email already exists.'))
        return email

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if not phone.isdigit() or len(phone) != 10 or len(set(phone)) == 1:
            raise ValidationError(_('Invalid phone number.'))
        return phone

    def clean_password(self):
        password = self.cleaned_data['password']
        # Add your custom password validation logic here
        if not any(char.isdigit() for char in password):
            raise ValidationError(_('Password must contain at least one digit.'))
        if not any(char.isupper() for char in password):
            raise ValidationError(_('Password must contain at least one uppercase letter.'))
        # Add more password validations as needed
        return password

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        # Check if password and confirm_password match
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', _('Passwords do not match.'))

        return cleaned_data
