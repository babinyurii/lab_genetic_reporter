from django.db import models
from users.models import CustomUser
from markers.models import SingleNucPol


class DetectionKit(models.Model):
    SNP = 'SNP'
    KIT_TYPE_CHOICES = (
        (SNP, 'in-house SNP assay'),
    )

    name = models.CharField(max_length=255, unique=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.PROTECT,
                                   null=True, blank=True)
    kit_type = models.CharField(max_length=20,
                                choices=KIT_TYPE_CHOICES, default='SNP')
    linked_markers = models.ManyToManyField(
                                    SingleNucPol,
                                    through='DetectionKitMarkers',
                                    related_name='detection_kits_list')

    class Meta:
        verbose_name = 'SNP detection kit'
        verbose_name_plural = 'SNP detection kits'

    def __str__(self):
        return self.name


class DetectionKitMarkers(models.Model):
    detection_kit = models.ForeignKey(DetectionKit,
                                      null=True, on_delete=models.SET_NULL)
    marker = models.ForeignKey(SingleNucPol,
                               null=True, on_delete=models.SET_NULL)

    class Meta:
        constraints = [models.UniqueConstraint(
                        fields=['detection_kit', 'marker', ],
                        name='detection_kit_marker_constraint')]
