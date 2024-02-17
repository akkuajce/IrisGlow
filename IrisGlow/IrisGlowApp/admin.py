from django.contrib import admin
from .models import CustomUser, UserProfile, Frame
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Frame)
