from django.contrib import admin
from patients.models import PatientSample, PatientSampleDetectionKit, ResultSNP, ReportRuleTwoSNP, ReportCombinations
from detection_kits.models import DetectionKit
from patients.models import ResultSNP


class PatientSampleDetectionKitInline(admin.TabularInline):
    model = PatientSampleDetectionKit
    extra = 1


class PatientSampleAdmin(admin.ModelAdmin):
    list_display = ('lab_id', 'last_name', 'first_name',  'date_sampled', 'date_delivered',
    'dna_concentration', 'dna_quality_260_280', 'dna_quality_260_230', 'notes', )
    list_display_links = ('lab_id', )
    inlines = (PatientSampleDetectionKitInline, )


class ResultSNPAdmin(admin.ModelAdmin):
    list_display = ('patient_sample',
                    'test',
                    'rs', 
                    'result',
                    'date_modified',)
    search_fields = ('patient_sample__last_name', 'rs',  )
    search_help_text = 'Search by last name or rs. Case sensitive. f.e. use "Иванов", not "иванов"'
    list_filter = ('test', )



admin.site.register(PatientSample, PatientSampleAdmin)
admin.site.register(ResultSNP, ResultSNPAdmin)
admin.site.register(ReportCombinations)
admin.site.register(ReportRuleTwoSNP)
