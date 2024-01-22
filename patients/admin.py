from django.contrib import admin
from patients.models import PatientSample, PatientSampleDetectionKit, ResultSNP
from detection_kits.models import DetectionKit
from patients.models import ResultSNP


class PatientSampleDetectionKitInline(admin.TabularInline):
    model = PatientSampleDetectionKit
    extra = 1


class PatientSampleAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'lab_id', 'date_sampled', 'date_delivered',
    'dna_concentration', 'dna_quality_260_280', 'dna_quality_260_230', 'notes', )
    inlines = (PatientSampleDetectionKitInline, )

class ResultSNPAdmin(admin.ModelAdmin):
    list_display = ('patient_sample',
                    'test',
                    'rs', 
                    'result',
                    'date_modified',)



admin.site.register(PatientSample, PatientSampleAdmin)
admin.site.register(ResultSNP, ResultSNPAdmin)
