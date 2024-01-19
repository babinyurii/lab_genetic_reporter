from django.contrib import admin
from patients.models import PatientSample, PatientSampleDetectionKit
from detection_kits.models import DetectionKit


class PatientSampleDetectionKitInline(admin.TabularInline):
    model = PatientSampleDetectionKit
    extra = 1


class PatientSampleAdmin(admin.ModelAdmin):
    list_display = ('first_name', )
    inlines = (PatientSampleDetectionKitInline, )



admin.site.register(PatientSample, PatientSampleAdmin)
