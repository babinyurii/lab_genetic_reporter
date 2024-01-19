from django.db import models
from patients.models import PatientSample
from detection_kits.models import DetectionKit

class ResultSNP(models.Model):
    patient_sample = models.ForeignKey(PatientSample, on_delete=models.CASCADE)
    test = models.ForeignKey(DetectionKit, on_delete=models.CASCADE)
    rs = models.CharField(max_length=20)
    result = models.CharField(max_length=2, blank=True, null=True)
    date_modified = models.DateTimeField(auto_now=True)
