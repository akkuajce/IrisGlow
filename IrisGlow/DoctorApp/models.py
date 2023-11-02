# from django.db import models
# from IrisGlowApp.models import CustomUser

# # Create your models here.
# class Doctor(models.Model):
#     bio = models.TextField(blank=True, null=True)
#     qualification = models.CharField(max_length=50, blank=True)
#     license = models.CharField(max_length=100, unique=True)
#     experience = models.IntegerField(blank=True,null=True)
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
#     speciality_name = models.ForeignKey(Specialities, on_delete=models.CASCADE, null=True)

#     def str(self):
#         return self.user.email
    
    

#     # Create your models here.
# class Specialities(models.Model):
#     speciality_name=models.CharField(max_length=100,unique=True)
#     symptoms = models.TextField(blank=True, null=True)
#     diagnosis = models.CharField(max_length=30)
#     treatments = models.TextField(blank=True, null=True)


    # status = models.BooleanField(default=True)
    # fees = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    # def str(self):
    #     return self.speciality_name

from django.db import models
from IrisGlowApp.models import CustomUser

# Create your models here.
class Specialities(models.Model):
    speciality_name = models.CharField(max_length=100, unique=True)
    symptoms = models.TextField(blank=True, null=True)
    diagnosis = models.CharField(max_length=30)
    treatments = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.speciality_name


class Doctor(models.Model):
    bio = models.TextField(blank=True, null=True)
    qualification = models.CharField(max_length=50, blank=True)
    license = models.CharField(max_length=100, unique=True)
    experience = models.IntegerField(blank=True, null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    speciality_name = models.ForeignKey(Specialities, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.email
