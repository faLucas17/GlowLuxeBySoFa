from django.contrib import admin
from .models import UserProfile, Address

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'newsletter', 'created_at']

@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['user', 'address_type', 'city', 'zip_code', 'is_default']