from django.contrib import admin

from .models import OTP


@admin.register(OTP)
class OTPAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone_number', 'email', 'otp_code', 'is_used', 'sent')
