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
    'dna_concentration', 'dna_quality_260_280', 'dna_quality_260_230', 'notes',) # 'tests')
    list_display_links = ('lab_id', )
    inlines = (PatientSampleDetectionKitInline, )
    search_fields = ('lab_id', 'last_name',)
    search_help_text = 'Search by lab_id or last name. Case sensitive. f.e. use "Иванов", not "иванов"'
    list_filter = ('tests', )
    """
    def tests(self, obj):
        return ", ".join([
            kit.name for kit in obj.tests.test.all()
        ])
    """
    

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
    list_display = ('name', 'detection_kits', 'snp_1', 'snp_2', 'order_in_conclusion',)
    #readonly_fields = ('detection_kits',)
    list_filter = ('tests', )
    

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == "snp_1":
            kwargs["queryset"] = SingleNucPol.objects.order_by('rs')
        if db_field.name == "snp_2":
            kwargs["queryset"] = SingleNucPol.objects.order_by('rs')
      
        return super().formfield_for_foreignkey(db_field, request, **kwargs)



class ReportCombinationsAdmin(admin.ModelAdmin):
    list_display = ('report_rule_two_snp', 'tests', 'snp_1', 'genotype_snp_1', 'snp_2', 'genotype_snp_2', 'report', )
    list_filter = ('report_rule_two_snp',)
    readonly_fields = ('report_rule_two_snp','snp_1', 'genotype_snp_1', 'snp_2', 'genotype_snp_2', )


    def tests(self, obj):
        return ', '.join([kit.name for kit in obj.report_rule_two_snp.tests.all()])

    def snp_1(self, obj):
        return obj.report_rule_two_snp.snp_1

    def snp_2(self, obj):
        return obj.report_rule_two_snp.snp_2

    def has_add_permission(self, request, obj=None):
        return False
    

class ConclusionSNPAdmin(admin.ModelAdmin):
    readonly_fields = ('test', 'patient', 'conclusion')
    search_fields = ('patient__last_name', 'patient__lab_id', 'test__name')
    search_help_text = 'search by patient last name, patient lab_id or kit name. case sensitive. use "Иванов", not "иванов"'

    def has_add_permission(self, request, obj=None):
        return False

    def changeform_view(self, request, object_id=None, form_url='', extra_context=None):
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        return super(ConclusionSNPAdmin, self).changeform_view(request, object_id, extra_context=extra_context)



admin.site.register(PatientSample, PatientSampleAdmin)
admin.site.register(ResultSNP, ResultSNPAdmin)
admin.site.register(ReportCombinations, ReportCombinationsAdmin)
admin.site.register(ReportRuleTwoSNP, ReportRuleTwoSNPAdmin)
admin.site.register(ConclusionSNP, ConclusionSNPAdmin)
