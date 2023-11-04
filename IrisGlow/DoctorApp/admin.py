from django.contrib import admin
from .models import Doctor, Specialities, Appointments

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Specialities)
admin.site.register(Appointments)


