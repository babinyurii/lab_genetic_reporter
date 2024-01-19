from django.db import models
from users.models import CustomUser
from markers.models import SingleNucPol


class DetectionKit(models.Model):
    SNP = 'SNP'
    KIT_TYPE_CHOICES = (
        (SNP, 'SNP'),
    )
    
    name = models.CharField(max_length=255)
    date_created = models.DateField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    markers = models.ManyToManyField(SingleNucPol)
    kit_type = models.CharField(max_length=20, choices=KIT_TYPE_CHOICES, default='SNP')

    
