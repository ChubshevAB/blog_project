from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
import re
from datetime import date


def validate_password_strength(value):
    if len(value) < 8:
        raise ValidationError("Пароль должен содержать не менее 8 символов.")
    if not re.search(r"\d", value):
        raise ValidationError("Пароль должен содержать хотя бы одну цифру.")


def validate_email_domain(value):
    allowed_domains = ["mail.ru", "yandex.ru"]
    domain = value.split("@")[-1]
    if domain not in allowed_domains:
        raise ValidationError(f'Разрешены только домены: {", ".join(allowed_domains)}')


class CustomUser(AbstractUser):
    email = models.EmailField(
        unique=True,
        validators=[validate_email_domain],
        error_messages={"unique": "Пользователь с таким email уже существует."},
    )
    phone = models.CharField(max_length=15, blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username

    def get_age(self):
        if self.birth_date:
            today = date.today()
            return (
                today.year
                - self.birth_date.year
                - (
                    (today.month, today.day)
                    < (self.birth_date.month, self.birth_date.day)
                )
            )
        return None
