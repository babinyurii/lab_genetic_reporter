from django.contrib import admin
from patients.models import PatientSample, PatientSampleDetectionKit, ResultSNP, ReportRuleTwoSNP, ReportCombinations, ConclusionSNP
from detection_kits.models import DetectionKit
from patients.models import ResultSNP
from patients.forms import ReportRuleForm # ResultSNPForm
from markers.models import SingleNucPol


class PatientSampleDetectionKitInline(admin.TabularInline):
    model = PatientSampleDetectionKit
    extra = 1


class PatientSampleAdmin(admin.ModelAdmin):
    list_display = ('lab_id', 'last_name', 'first_name',  'date_sampled', 'date_delivered',
    'dna_concentration', 'dna_quality_260_280', 'dna_quality_260_230', 'notes', )
    list_display_links = ('lab_id', )
    inlines = (PatientSampleDetectionKitInline, )


class ResultSNPAdmin(admin.ModelAdmin):
    readonly_fields = ('patient_sample', 'test', 'rs')

    list_display = ('patient_sample', 
                    'test',
                    'rs', 
                    'result',
                    'date_modified',)
    search_fields = ('patient_sample__last_name', 'rs__rs',  )
    search_help_text = 'Search by last name or rs. Case sensitive. f.e. use "Иванов", not "иванов"'
    list_filter = ('test', )


    def has_add_permission(self, request, obj=None):
        return False

   

class ReportRuleTwoSNPAdmin(admin.ModelAdmin):
    form = ReportRuleForm

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "snp_1":
            kwargs["queryset"] = SingleNucPol.objects.order_by('rs')
        if db_field.name == "snp_2":
            kwargs["queryset"] = SingleNucPol.objects.order_by('rs')
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class ReportCombinationsAdmin(admin.ModelAdmin):
    list_display = ('report_rule_two_snp', 'tests', 'genotype_snp_1', 'genotype_snp_2', 'report', )
    list_filter = ('report_rule_two_snp',)
    readonly_fields = ('report_rule_two_snp', 'genotype_snp_1', 'genotype_snp_2', )

    def tests(self, obj):
        return ', '.join([kit.name for kit in obj.report_rule_two_snp.tests.all()])

    def has_add_permission(self, request, obj=None):
        return False
    

class ConclusionSNPAdmin(admin.ModelAdmin):
    readonly_fields = ('test', 'patient')
    search_fields = ('patient',)
    search_help_text = 'search by patient. case sensitive. use "Иванов", not "иванов"'

    def has_add_permission(self, request, obj=None):
        return False



admin.site.register(PatientSample, PatientSampleAdmin)
admin.site.register(ResultSNP, ResultSNPAdmin)
admin.site.register(ReportCombinations, ReportCombinationsAdmin)
admin.site.register(ReportRuleTwoSNP, ReportRuleTwoSNPAdmin)
admin.site.register(ConclusionSNP, ConclusionSNPAdmin)
