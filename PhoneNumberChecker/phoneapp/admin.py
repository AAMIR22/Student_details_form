from django.contrib import admin

# Register your models here.
from .models import PhoneNumber, ExtendedUser

admin.site.register(PhoneNumber)
admin.site.register(ExtendedUser)
