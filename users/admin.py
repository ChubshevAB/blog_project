from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ["username", "email", "phone", "birth_date", "created_at"]
    list_filter = ["is_staff", "is_active", "created_at"]
    search_fields = ["username", "email", "phone"]
    fieldsets = UserAdmin.fieldsets + (
        ("Дополнительная информация", {"fields": ("phone", "birth_date")}),
    )
