from django.db import models
from users.models import CustomUser


class DetectionKit(models.Model):
    name = models.CharField(max_length=255)
    date_created = models.DateField()
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    
