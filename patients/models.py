from django.db import models
from users.models import CustomUser
from detection_kits.models import DetectionKit
from datetime import datetime
from django.core.validators import MinValueValidator



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
    rs = models.CharField(max_length=20)
    result = models.CharField(max_length=2, blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)


    def __str__(self):
        return f'{self.patient_sample}. SNP: {self.rs}. result: {self.result}'

    
    class Meta:
        verbose_name = 'SNP result'
        verbose_name_plural = 'SNP results'




class ReportRuleTwoSNP(models.Model):
    name = models.CharField(max_length=255)
    snp_1 = models.CharField(max_length=20)
    snp_2 = models.CharField(max_length=20)
    note = models.TextField(max_length=1000)
    tests = models.ManyToManyField(DetectionKit, related_name='report_rules')


    """
    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)
        record_pk = self.pk

        kit_markers = self.test.markers.all()
    """



class ReportCombinations(models.Model):
    report_rule_two_snp = models.ForeignKey(ReportRuleTwoSNP, on_delete=models.CASCADE)
    snp_1_var_both_strands = models.CharField(max_length=2, blank=True, null=True)
    snp_2_var_both_strands = models.CharField(max_length=2, blank=True, null=True)
    report = models.TextField(max_length=1000)

        
    

