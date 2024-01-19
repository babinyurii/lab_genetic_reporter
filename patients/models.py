from django.db import models
from users.models import CustomUser
from detection_kits.models import DetectionKit
from datetime import datetime



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

    """
    def save(self, *args, **kwargs):

        print("*" * 100, flush=True)
        
        super().save(*args, **kwargs)
        print('self.tests: ', self.tests)
        patient_sample = PatientSample.objects.get(pk=self.pk)
        detection_kits = patient_sample.tests.all()

        print('self.pk: ', patient_sample)
        print('self.tests: ', detection_kits)
    """
        
    



class PatientSampleDetectionKit(models.Model):
    patient_sample = models.ForeignKey(PatientSample, on_delete=models.PROTECT)
    test = models.ForeignKey(DetectionKit, on_delete=models.PROTECT)
    date_created = models.DateTimeField(auto_now_add=True)


    def save(self, *args, **kwargs):
        
        super().save(*args, **kwargs)

        print("*" * 100, flush=True)
        record_pk = self.pk
        print('current pk: ', record_pk)
        print('self.patient: ', self.patient_sample)
        print('self.test: ', self.test)
        print('markers: ', self.test.markers.all())
        
    

