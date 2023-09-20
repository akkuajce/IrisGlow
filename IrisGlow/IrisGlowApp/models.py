
from django.db import models
from datetime import date
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, phone, email, password=None):
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone, 
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name, last_name ,phone, email, password=None):
        
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
           first_name=first_name,
            last_name=last_name,
            phone=phone,
        )
        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        user.role=4
        user.save(using=self._db)
        return user

class CustomUser(AbstractUser):
    PATIENT = 1
    DOCTOR = 2
    SPECTS = 3
    ADMIN = 4

    ROLE_CHOICE = (
        (PATIENT, 'Patient'),
        (DOCTOR, 'Doctor'),
        (SPECTS, 'Spects'),
        (ADMIN,'Admin'),
    )

    username=None
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    USERNAME_FIELD = 'email'
    email = models.EmailField(max_length=100, unique=True)
    phone = models.CharField(max_length=12, blank=True)
    password = models.CharField(max_length=128)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True,default='1')


    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_superadmin = models.BooleanField(default=False)

    
    REQUIRED_FIELDS = ['first_name','last_name', 'phone']

    objects = UserManager()

    def _str_(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True



class UserProfile(models.Model):

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    addressline1 = models.CharField(max_length=50, blank=True, null=True)
    addressline2 = models.CharField(max_length=50, blank=True, null=True)
    # country = models.CharField(max_length=15, default="India", blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    state = models.CharField(max_length=50, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(max_length=50, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    profile_created_at = models.DateTimeField(auto_now_add=True)
    profile_modified_at = models.DateTimeField(auto_now=True)


    def calculate_age(self):
        today = date.today()
        age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
        return age
    age = property(calculate_age)


    def get_gender_display(self):
        return dict(self.GENDER_CHOICES).get(self.gender)

    def _str_(self):
        return self.user.email
    
    def get_role(self): 
        if self.role == 1:
            user_role = 'Patient'
        elif self.role == 2:
            user_role = 'Doctor'
        elif self.role == 3:
            user_role = 'Spects'
        return user_role