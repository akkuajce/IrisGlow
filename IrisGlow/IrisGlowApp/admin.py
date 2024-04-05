from django.contrib import admin
from .models import CustomUser, UserProfile, Frame, PaymentP, UserCart, ShippingAddress
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(UserProfile)
admin.site.register(Frame)
admin.site.register(PaymentP)
admin.site.register(UserCart)
admin.site.register(ShippingAddress)