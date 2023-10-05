from django import forms
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
            'first_name': BootstrapTextInput(attrs={'placeholder': 'Enter Your Name', 'id': 'first_name'}),
            'last_name': BootstrapTextInput(attrs={'placeholder': 'Enter Your Name', 'id': 'last_name'}),
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
            # 'profile_picture': BootstrapFileInput(attrs={'placeholder': 'Upload Profile Picture'}),
            # 'profile_picture': forms.ClearableFileInput(attrs={'class': 'custom-file-input'}),
            'address': BootstrapTextInput(attrs={'placeholder': 'Address Line 1', 'id': 'address'}),
            'addressline1': BootstrapTextInput(attrs={'placeholder': 'Address Line 2', 'id': 'address1'}),
            'addressline2': BootstrapTextInput(attrs={'placeholder': 'Address Line 3', 'id': 'address2'}),
            'country': BootstrapSelect(attrs={'placeholder': 'Select Country', 'id': 'country'}),
            'state': BootstrapSelect(attrs={'placeholder': 'Select State', 'id': 'state'}),
            'city': BootstrapTextInput(attrs={'placeholder': 'Enter City', 'id': 'city'}),
            'pin_code': BootstrapTextInput(attrs={'placeholder': 'Enter Pin Code', 'id': 'zipcode'}),
            'gender': BootstrapSelect(attrs={'placeholder': 'Select Gender', 'id': 'gender'}),
            # 'dob': forms.DateInput(attrs={'placeholder': 'Select Date of Birth', 'id': 'dob'}),
        }