from django.db import models
from IrisGlowApp.models import CustomUser

# Create your models here.
class Doctor(models.Model):
    bio = models.TextField(blank=True, null=True)
    qualification = models.CharField(max_length=50, blank=True)
    license = models.CharField(max_length=100, unique=True)
    experience = models.IntegerField(blank=True,null=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, blank=True, null=True)
    #therapy = models.ForeignKey(Therapy, on_delete=models.CASCADE, null=True)

    def str(self):
        return self.user.email