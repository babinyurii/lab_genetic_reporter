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


class ReportRuleTwoSNPAdmin(admin.ModelAdmin):
    list_display = ('name', 'snp_1', 'snp_2', 'note', )
    list_filter = ('tests',)

    
    #def tests(self, obj):
    #    return ', '.join([kit.name for kit in obj.tests.all()])
    

class ReportCombinationsAdmin(admin.ModelAdmin):
    list_display = ('report_rule_two_snp', 'tests', 'genotype_snp_1', 'genotype_snp_2', 'report', )
    list_filter = ('report_rule_two_snp',)

    def tests(self, obj):
        return ', '.join([kit.name for kit in obj.report_rule_two_snp.tests.all()])
    
    # пока в объекте report_rule_two_snp строки, а не ссылки на объекты
    # попробовать после, когда может быть будут ссылки на сами объекты
    """
    def snp_1(self, obj):
        rs_snp_1 = obj.report_rule_two_snp.snp_1
    """




admin.site.register(PatientSample, PatientSampleAdmin)
admin.site.register(ResultSNP, ResultSNPAdmin)
admin.site.register(ReportCombinations, ReportCombinationsAdmin)
admin.site.register(ReportRuleTwoSNP, ReportRuleTwoSNPAdmin)
