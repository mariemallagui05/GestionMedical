
from django.contrib import admin
from django.utils import timezone
from datetime import timedelta
from .models import Appointment



class AppointmentInline(admin.StackedInline):
    model = Appointment
    extra = 0


class DateRangeFilter(admin.SimpleListFilter):
    title = 'Date du rendez-vous'
    parameter_name = 'date_range'

    def lookups(self, request, model_admin):
        return [
            ('today', "Aujourd'hui"),
            ('week', 'Cette semaine'),
            ('upcoming', 'À venir'),
        ]

    def queryset(self, request, queryset):
        now = timezone.now()

        if self.value() == 'today':
            return queryset.filter(appointment_date__date=now.date())

        if self.value() == 'week':
            start = now - timedelta(days=now.weekday())
            end = start + timedelta(days=7)
            return queryset.filter(
                appointment_date__gte=start,
                appointment_date__lt=end
            )

        if self.value() == 'upcoming':
            return queryset.filter(appointment_date__gte=now)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):

    list_display = (
        'appointment_date',
        'doctor',
        'patient',
        'duration_minutes',
        'status'
    )

    list_filter = ('status', 'doctor', DateRangeFilter)

    search_fields = (
        'patient__last_name',
        'patient__national_id',
        'doctor__last_name',
        'doctor__license_number'
    )

    ordering = ('-appointment_date',)

    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Participants', {
            'fields': ('doctor', 'patient')
        }),
        ('Planification', {
            'fields': ('appointment_date', 'duration_minutes', 'status')
        }),
        ('Dossier', {
            'fields': ('reason', 'prescription')
        }),
        ('Suivi', {
            'fields': ('created_at', 'updated_at')
        }),
    )

    @admin.action(description="Confirmer les rendez-vous sélectionnés")
    def confirm_appointments(self, request, queryset):
        queryset.update(status=Appointment.Status.CONFIRMED)

    @admin.action(description="Annuler les rendez-vous sélectionnés")
    def cancel_appointments(self, request, queryset):
        queryset.update(status=Appointment.Status.CANCELLED)

    actions = ['confirm_appointments', 'cancel_appointments']
