from django.db import models
from users.models import CustomUser
from detection_kits.models import DetectionKit

class PatientSample(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    middle_name = models.CharField(max_length=255, blank=True, null=True)
    age = models.PositiveIntegerField()
    clinic_id = models.CharField(max_length=255, blank=True, null=True)
    lab_id = models.CharField(max_length=255)
    date_sampled = models.DateField(blank=True, null=True)
    date_delivered = models.DateField()
    dna_concentration = models.PositiveIntegerField()
    dna_quality_260_280 = models.FloatField()
    dna_quality_260_230 = models.FloatField()
    notes = models.TextField(max_length=255)
    created_by = models.ForeignKey(CustomUser, null=True, blank=True, on_delete=models.PROTECT)
    tests = models.ManyToManyField(DetectionKit, through='PatientSampleDetectionKit')




class PatientSampleDetectionKit(models.Model):
    patient_sample = models.ForeignKey(PatientSample, on_delete=models.PROTECT)
    test = models.ForeignKey(DetectionKit, on_delete=models.PROTECT)
    rs = models.CharField(max_length=20, null=True, blank=True)
    rs_result = models.CharField(max_length=2, null=True, blank=True)
