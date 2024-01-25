from django.db import models
from users.models import CustomUser
from markers.models import SingleNucPol


class DetectionKit(models.Model):
    SNP = 'SNP'
    KIT_TYPE_CHOICES = (
        (SNP, 'in-house SNP assay'),
    )
    
    name = models.CharField(max_length=255, unique=True)
    date_created = models.DateField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    markers = models.ManyToManyField(SingleNucPol)
    kit_type = models.CharField(max_length=20, choices=KIT_TYPE_CHOICES, default='SNP')
    

    class Meta:
        verbose_name = 'SNP detection kit'
        verbose_name_plural = 'SNP detection kits'


    def __str__(self):
        return self.name
    

    
