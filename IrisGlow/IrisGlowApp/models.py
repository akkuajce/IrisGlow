
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

    GENDER_CHOICES = (
        ('F', 'Female'),
        ('M', 'Male'),
        ('NB', 'Non Binary'),
        ('TF', 'Transfeminine'),
        ('TM', 'Transmasculine'),
    )

    STATE_CHOICES = [
        ('Andhra Pradesh', 'Andhra Pradesh'),
        ('Arunachal Pradesh', 'Arunachal Pradesh'),
        ('Assam', 'Assam'),
        ('Bihar', 'Bihar'),
        ('Chhattisgarh', 'Chhattisgarh'),
        ('Goa', 'Goa'),
        ('Gujarat', 'Gujarat'),
        ('Haryana', 'Haryana'),
        ('Himachal Pradesh', 'Himachal Pradesh'),
        ('Jharkhand', 'Jharkhand'),
        ('Karnataka', 'Karnataka'),
        ('Kerala', 'Kerala'),
        ('Madhya Pradesh', 'Madhya Pradesh'),
        ('Maharashtra', 'Maharashtra'),
        ('Manipur', 'Manipur'),
        ('Meghalaya', 'Meghalaya'),
        ('Mizoram', 'Mizoram'),
        ('Nagaland', 'Nagaland'),
        ('Odisha', 'Odisha'),
        ('Punjab', 'Punjab'),
        ('Rajasthan', 'Rajasthan'),
        ('Sikkim', 'Sikkim'),
        ('Tamil Nadu', 'Tamil Nadu'),
        ('Telangana', 'Telangana'),
        ('Tripura', 'Tripura'),
        ('Uttar Pradesh', 'Uttar Pradesh'),
        ('Uttarakhand', 'Uttarakhand'),
        ('West Bengal', 'West Bengal'),
    ]

    ASIAN_COUNTRY_CHOICES = [
    ('India', 'India'),
    ]





    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='media/profile_picture', blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    addressline1 = models.CharField(max_length=50, blank=True, null=True)
    addressline2 = models.CharField(max_length=50, blank=True, null=True)
    
    country = models.CharField(max_length=50, choices=ASIAN_COUNTRY_CHOICES, default='India', blank=True, null=True)
    state = models.CharField(("Select State"),max_length=40, choices=STATE_CHOICES, blank=True, null=True)
    city = models.CharField(max_length=50, blank=True, null=True)
    pin_code = models.CharField(max_length=50, blank=True, null=True)
    gender = models.CharField(("Select Gender"),max_length=4, choices=GENDER_CHOICES, blank=True, null=True)

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
    
    def __str__(self):
        return self.user.email
    




from django.db import models
from django.core.validators import MaxValueValidator

class Frame(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
        ('K', 'Kids'),
    )

    CATEGORY_CHOICES = (
        ('Eyeglasses', 'Eyeglasses'),
        ('Sunglasses', 'Sunglasses'),
        ('Computer Glasses', 'Computer Glasses'),
    )

    FRAME_MATERIAL_CHOICES = (
        ('Metal', 'Metal'),
        ('Plastic', 'Plastic'),
        ('Wood', 'Wood'),
        ('Aluminium', 'Aluminium'),
        ('Glass', 'Glass'),
        # Add more as needed
    )

    FRAME_STYLE_CHOICES = (
        ('Circle', 'Circle'),
        ('Rectangle', 'Rectangle'),
        ('Geometric', 'Geometric'),
        ('Square', 'Square'),
        # Add more as needed
    )

    SIZE_CHOICES = (
        ('Small', 'Small'),
        ('Medium', 'Medium'),
        ('Large', 'Large'),
    )

    BRAND_CHOICES = (
        ('Fastrack', 'Fastrack'),
        ('Titan', 'Titan'),
        ('Essilor', 'Essilor'),
        ('Ray-Ban', 'Ray-Ban'),
        ('Boss', 'Boss'),
        ('Polaroid', 'Polaroid'),
        ('Vogue', 'Vogue'),
        # Add more as needed
    )

    COLOR_CHOICES = (
        ('Red', 'Red'),
        ('Blue', 'Blue'),
        ('Green', 'Green'),
        ('Black', 'Black'),
        ('White', 'White'),
        # Add more as needed
    )

    TEMPLE_LENGTH_CHOICES = [
        ('140', '140 mm'),
        ('141', '141 mm'),
        ('142', '142 mm'),
        ('143', '143 mm'),
        ('144', '144 mm'),
        ('145', '145 mm'),
        ('146', '146 mm'),
        ('147', '147 mm'),
        ('148', '148 mm'),
        ('149', '149 mm'),
        ('150', '150 mm'),
        ('151', '151 mm'),
        ('152', '152 mm'),
        ('153', '153 mm'),
        ('154', '154 mm'),
        ('155', '155 mm'),
        ('156', '156 mm'),
        ('157', '157 mm'),
        ('158', '158 mm'),
        # Add more choices up to '155' if needed
    ]

    BRIDGE_SIZE_CHOICES = [
        ('15', '15 mm'),
        ('16', '16 mm'),
        ('17', '17 mm'),
        ('18', '18 mm'),
        ('19', '19 mm'),
        ('20', '20 mm'),
        ('21', '21 mm'),
        ('22', '22 mm'),
        ('23', '23 mm'),
        ('24', '24 mm'),
        ('25', '25 mm'),
        # Add more choices up to '25' if needed
    ]

    LENS_WIDTH_CHOICES = [
        ('45', '45 mm'),
        ('46', '46 mm'),
        ('47', '47 mm'),
        ('48', '48 mm'),
        ('49', '49 mm'),
        ('50', '50 mm'),
        ('51', '51 mm'),
        ('52', '52 mm'),
        ('53', '53 mm'),
        ('54', '54 mm'),
        ('55', '55 mm'),
        ('56', '56 mm'),
        ('57', '57 mm'),
        ('58', '58 mm'),
        # Add more choices up to '58' if needed
    ]

    name = models.CharField(max_length=255, unique=True)
    brand_name = models.CharField(max_length=255, choices=BRAND_CHOICES)
    category = models.CharField(max_length=255, choices=CATEGORY_CHOICES)
    product_description = models.TextField()
    material_description = models.TextField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2, validators=[MaxValueValidator(10000)])
    stock_quantity = models.PositiveIntegerField(default=0)
    production_date = models.DateField(null=True, blank=True)
   
    color = models.CharField(max_length=50, null=True, blank=True, choices=COLOR_CHOICES)
    size = models.CharField(max_length=10, choices=SIZE_CHOICES, null=True, blank=True)

    # Eye Frames Specific Fields
    frame_material = models.CharField(max_length=20, choices=FRAME_MATERIAL_CHOICES, null=True, blank=True)
    frame_style = models.CharField(max_length=20, choices=FRAME_STYLE_CHOICES, null=True, blank=True)
    temple_length = models.CharField(max_length=3, choices=TEMPLE_LENGTH_CHOICES, default='15')
    bridge_size = models.CharField(max_length=5, choices=BRIDGE_SIZE_CHOICES, default='15')
    lens_width = models.CharField(max_length=5, choices=LENS_WIDTH_CHOICES, default='15')

    # Thumbnail and Additional Images
    thumbnail = models.ImageField(upload_to='frame_thumbnails/')
    image_2 = models.ImageField(upload_to='frame_images/', blank=True, null=True)
    image_3 = models.ImageField(upload_to='frame_images/', blank=True, null=True)
    image_4 = models.ImageField(upload_to='frame_images/', blank=True, null=True)
    image_5 = models.ImageField(upload_to='frame_images/', blank=True, null=True)

    # AutoField for frame_id
    frame_id = models.AutoField(primary_key=True, unique=True)

    def __str__(self):
        return self.name







from django.db import models
from .models import Frame
from django.contrib.auth import get_user_model

User = get_user_model()

class UserCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    frame = models.ForeignKey(Frame, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)




    

    def total_price(self):
        return self.frame.price * self.quantity

    def __str__(self):
        return f"{self.frame.name} - {self.quantity}"




