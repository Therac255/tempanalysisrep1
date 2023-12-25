from django.contrib import admin

from .models import Buyer


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user_first_name",
        "user_last_name",
        "patronymic",
        "verification_state",
        "issuing_body",
        "issue_date",
        "document_number",
        "phone_number",
        "is_active",
        "country",
        "user_email",
        "tax_id",
    )
    search_fields = [
        "user__personal_info__first_name",
        "user__personal_info__last_name",
        "user__personal_info__patronymic",
        "user__email",
        "tax_id"]
    list_filter = [
        "user__is_active",
        "user__personal_info__verification_state",
        "user__personal_info__country",
    ]

    @staticmethod
    def user_first_name(obj):
        if obj.user and obj.user.personal_info:
            return obj.user.personal_info.first_name
        return ''

    @staticmethod
    def user_last_name(obj):
        if obj.user and obj.user.personal_info:
            return obj.user.personal_info.last_name
        return ''

    @staticmethod
    def patronymic(obj):
        if obj.user and obj.user.personal_info:
            return obj.user.personal_info.patronymic
        return ''

    @staticmethod
    def verification_state(obj):
        if obj.user and obj.user.personal_info:
            return obj.user.personal_info.verification_state
        return ''

    @staticmethod
    def issuing_body(obj):
        if obj.user and obj.user.personal_info:
            return obj.user.personal_info.issuing_body
        return ''

    @staticmethod
    def issue_date(obj):
        if obj.user and obj.user.personal_info:
            return obj.user.personal_info.issue_date
        return ''

    @staticmethod
    def document_number(obj):
        if obj.user and obj.user.personal_info:
            return obj.user.personal_info.document_number
        return ''

    @staticmethod
    def phone_number(obj):
        if obj.user and obj.user.personal_info:
            return obj.user.personal_info.phone_number
        return ''

    @staticmethod
    def is_active(obj):
        if obj.user:
            return obj.user.is_active
        return ''

    @staticmethod
    def country(obj):
        if obj.user and obj.user.personal_info and obj.user.personal_info.country:
            return obj.user.personal_info.country.name
        return ''

    @staticmethod
    def user_email(obj):
        if obj.user:
            return obj.user.email
        return ''
