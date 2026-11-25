
from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from AccountApp.models import Doctor, Patient


class Appointment(models.Model):

    class Status(models.TextChoices):
        PENDING = 'PENDING', 'En attente'
        CONFIRMED = 'CONFIRMED', 'Confirmé'
        CANCELLED = 'CANCELLED', 'Annulé'

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name='appointments'
    )

    appointment_date = models.DateTimeField()

    reason = models.TextField()

    prescription = models.FileField(
        upload_to='prescriptions/',
        blank=True,
        null=True
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    duration_minutes = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['appointment_date']
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'appointment_date'],
                name='unique_doctor_appointment'
            )
        ]

    def clean(self):
        super().clean()

        if self.appointment_date:
            if self._state.adding or (
                self.pk and self._date_changed()
            ):
                if self.appointment_date <= timezone.now():
                    raise ValidationError({
                        'appointment_date':
                        "La date du rendez-vous doit être future."
                    })

    def _date_changed(self):
        old = Appointment.objects.get(pk=self.pk)
        return old.appointment_date != self.appointment_date

    def __str__(self):
        return f"{self.patient} - Dr {self.doctor} - {self.appointment_date}"
