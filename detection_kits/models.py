from django.db import models
from users.models import CustomUser
from markers.models import SingleNucPol


class DetectionKit(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT, null=True, blank=True)
    markers = models.ManyToManyField(SingleNucPol)

    
