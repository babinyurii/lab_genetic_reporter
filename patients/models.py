from django.db import models
from users.models import CustomUser
from detection_kits.models import DetectionKit
from datetime import datetime
from django.core.validators import MinValueValidator
from markers.models import SingleNucPol
from django.core.exceptions import ValidationError


def check_if_rs_exists(value):
    if not SingleNucPol.objects.filter(rs=value).exists():
        raise ValidationError('this rs id does not exist in the database. please, check "MARKERS" application.')


class PatientSample(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField()
    clinic_id = models.CharField(max_length=255, blank=True, null=True)
    lab_id = models.CharField(max_length=255, unique=True)
    date_sampled = models.DateField(blank=True, null=True)
    date_delivered = models.DateField()
    dna_concentration = models.PositiveIntegerField(validators=[MinValueValidator(0)])
    dna_quality_260_280 = models.FloatField()
    dna_quality_260_230 = models.FloatField()
    notes = models.TextField(max_length=255)
    created_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.PROTECT)
    tests = models.ManyToManyField(DetectionKit, through='PatientSampleDetectionKit')


    def __str__(self):
        return f'{self.last_name} {self.first_name}'


    class Meta:
        verbose_name = 'Sample'
        verbose_name_plural = 'Samples'
    

        

class PatientSampleDetectionKit(models.Model):
    patient_sample = models.ForeignKey(PatientSample, on_delete=models.PROTECT,)
    test = models.ForeignKey(DetectionKit, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        record_pk = self.pk

        kit_markers = self.test.markers.all()

        for marker in kit_markers:
            if not ResultSNP.objects.filter(
                rs=marker.rs, 
                test=self.test.pk, 
                patient_sample=self.patient_sample.pk).exists():
                
                ResultSNP.objects.create(
                    patient_sample=self.patient_sample,
                    test=self.test,
                    rs=marker.rs,
                    result=None
                )

    def __str__(self):
        return f'{self.test}'

    class Meta:
        verbose_name = 'Detection kit'
        verbose_name_plural = 'Detection kits'
        constraints = [models.UniqueConstraint(fields=['patient_sample', 'test', ], name='patient_and_test_unique_constraint')]


class ResultSNP(models.Model):
    patient_sample = models.ForeignKey(PatientSample, on_delete=models.CASCADE)
    test = models.ForeignKey(DetectionKit, on_delete=models.CASCADE)
    rs = models.CharField(max_length=20, validators=[check_if_rs_exists,])
    result = models.CharField(max_length=2, blank=True, null=True, help_text='use only English characters for result')
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'SNP result'
        verbose_name_plural = 'SNP results'

    def __str__(self):
        return f'{self.patient_sample}. SNP: {self.rs}. result: {self.result}'


    def save(self, *args, **kwargs):
        update_obj = False
        print('self.pk before save: ', self.pk, flush=True)        
        if self.pk:
            update_obj = True
        
        super().save(*args, **kwargs)
        print(ResultSNP.objects.filter(
            test=self.test,
            patient_sample=self.patient_sample,
        ))

        if update_obj: # look for conclusion creation only when snp results are updated,
            # not created automatically after patient creation
            results_snp = ResultSNP.objects.filter(
                test=self.test,
                patient_sample=self.patient_sample)

            results = [obj.result for obj in results_snp]
            print('results: ', results)

            if all(results):
                print('generating report')
                text = ''
                test = self.test
                rules = ReportRuleTwoSNP.objects.filter(
                    tests=self.test
                )
                for rule in rules:
                    combs = ReportCombinations.objects.filter(
                        report_rule_two_snp=rule
                    )
                    print('combs: ', combs)
                    snp_1_rs = rule.snp_1
                    snp_2_rs = rule.snp_2
                    snp_1_result = results_snp.get(rs=snp_1_rs).result
                    snp_2_result = results_snp.get(rs=snp_2_rs).result
                    print('snp_1_result: ', snp_1_result, '  snp_2_result: ', snp_2_result)
                    for comb in combs:
                        print('comb genotype 1: ', comb.genotype_snp_1, 'comb genotype 2: ', comb.genotype_snp_2)
                    conclusion_for_result = combs.get(genotype_snp_1=snp_1_result,
                                                              genotype_snp_2=snp_2_result)
                    text += conclusion_for_result.report
                    print(text)
                if not ConclusionSNP.objects.filter(patient=self.patient_sample, test=self.test).exists():
                    ConclusionSNP.objects.create(patient=self.patient_sample,
                                                test=self.test, conclusion=text )
                else:
                    conc_obj = ConclusionSNP.objects.get(patient=self.patient_sample, test=self.test)
                    conc_obj.conclusion = text
                    conc_obj.save()


    





class ReportRuleTwoSNP(models.Model):
    name = models.CharField(max_length=255)
    snp_1 = models.CharField(max_length=20)
    snp_2 = models.CharField(max_length=20)
    note = models.TextField(max_length=1000)
    tests = models.ManyToManyField(DetectionKit, related_name='report_rules')


    
    def __str__(self):
        return self.name


    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

        snp_1 = SingleNucPol.objects.get(rs=self.snp_1)
        snp_2 = SingleNucPol.objects.get(rs=self.snp_2)

        genotypes_snp_1 = [snp_1.nuc_var_1 + snp_1.nuc_var_1,
                    snp_1.nuc_var_1 + snp_1.nuc_var_2,
                    snp_1.nuc_var_2 + snp_1.nuc_var_2]
        genotypes_snp_2 = [snp_2.nuc_var_1 + snp_2.nuc_var_1,
                    snp_2.nuc_var_1 + snp_2.nuc_var_2,
                    snp_2.nuc_var_2 + snp_2.nuc_var_2]

        for genotype_snp_1 in genotypes_snp_1:
            for genotype_snp_2 in genotypes_snp_2:
                if not ReportCombinations.objects.filter(
                            report_rule_two_snp=self,
                            genotype_snp_1=genotype_snp_1,
                            genotype_snp_2=genotype_snp_2).exists():
                    ReportCombinations.objects.create(
                            report_rule_two_snp=self,
                            genotype_snp_1=genotype_snp_1,
                            genotype_snp_2=genotype_snp_2)

    




class ReportCombinations(models.Model):
    report_rule_two_snp = models.ForeignKey(ReportRuleTwoSNP, on_delete=models.CASCADE)
    genotype_snp_1 = models.CharField(max_length=2, blank=True, null=True)
    genotype_snp_2 = models.CharField(max_length=2, blank=True, null=True)
    report = models.TextField(max_length=1000, blank=True, null=True)

    class Meta:
        verbose_name = 'report rules: conclusions for genotype combinations'
        verbose_name_plural = 'report rules: conclusions for genotype combinations'

    def __str__(self):
        return self.report_rule_two_snp.name


class ConclusionSNP(models.Model):
    patient = models.ForeignKey(PatientSample, on_delete=models.CASCADE)
    test = models.ForeignKey(DetectionKit, on_delete=models.CASCADE)
    conclusion = models.TextField(max_length=5000)

    class Meta:
        verbose_name = 'conclusion for report'
        verbose_name_plural = 'conclusions for reports'

    def __str__(self):
        return f'conclusion for: {self.patient}, test: {self.test}'
    

    
     
    

    
    

        
    

