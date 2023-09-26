from django import forms
from django.contrib.auth import get_user_model
#from .models import UserProfile
#from therapist.models import Therapist

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