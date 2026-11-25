from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, RegexValidator
from django.db import models
from django.utils import timezone


phone_validator = RegexValidator(
    r'^\d{8}$',
    "Le téléphone doit contenir exactement 8 chiffres.",
)

cin_validator = RegexValidator(
    r'^\d{8}$',
    "Le CIN doit contenir exactement 8 chiffres.",
)


def validate_past_date(value):
    if value >= timezone.localdate():
        raise ValidationError(
            "La date de naissance doit être antérieure à la date du jour."
        )


class User(AbstractUser):
    pass


class Specialty(models.Model):
    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "Specialties"

    def __str__(self):
        return self.name


class Doctor(User):
    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)],
    )
    phone = models.CharField(max_length=8, validators=[phone_validator])
    specialties = models.ManyToManyField(
        Specialty,
        related_name="doctors",
        blank=True,
    )

    class Meta:
        verbose_name = "Doctor"

    def __str__(self):
        return f"Dr {self.first_name} {self.last_name}"


class Patient(User):
    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[cin_validator],
    )
    phone = models.CharField(max_length=8, validators=[phone_validator])
    birth_date = models.DateField(validators=[validate_past_date])

    class Meta:
        verbose_name = "Patient"

    def clean(self):
        super().clean()
        if self.birth_date and self.birth_date >= timezone.localdate():
            raise ValidationError(
                {"birth_date": "La date de naissance doit être dans le passé."}
            )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"