
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User, Doctor, Patient, Specialty
from AppointmentApp.admin import AppointmentInline



@admin.register(Specialty)
class SpecialtyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    ordering = ('name',)





@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):

    list_display = ('last_name', 'first_name', 'license_number', 'phone')
    list_filter = ('specialties',)
    search_fields = ('license_number', 'last_name', 'first_name')
    ordering = ('last_name',)

    fields = (
        'username',
        'password',
        'email',
        'first_name',
        'last_name',
        'license_number',
        'phone',
        'specialties',
    )






@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):

    list_display = (
        'last_name', 'first_name', 'national_id',
        'phone', 'birth_date'
    )

    search_fields = ('last_name', 'first_name', 'national_id')
    ordering = ('last_name',)
    inlines = [AppointmentInline]

    fields = (
        'username',
        'email',
        'first_name',
        'last_name',
        'national_id',
        'phone',
        'birth_date',
    )




