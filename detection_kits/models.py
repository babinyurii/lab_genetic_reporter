from django.db import models
from users.models import CustomUser
from markers.models import SingleNucPol
from django.template.defaultfilters import truncatewords
from django.core.exceptions import ValidationError


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
        verbose_name_plural = '1. SNP detection kits'

    def __str__(self):
        return f'{self.name}'




class DetectionKitMarkers(models.Model):
    ORDER_FOR_CONCLUSION = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    )

    ORDER = (
        (1, 1),
        (2, 2),
        (3, 3),
        (4, 4),
        (5, 5),
        (6, 6),
        (7, 7),
        (8, 8),
        (9, 9),
        (10, 10),
    )
    detection_kit = models.ForeignKey(DetectionKit,
                                      null=True, on_delete=models.SET_NULL)
    marker = models.ForeignKey(SingleNucPol,
                               null=True, on_delete=models.SET_NULL)
    marker_category_in_kit = models.CharField(max_length=50, blank=True, null=True)
    category_order_in_conclusion = models.IntegerField(choices=ORDER, null=True, blank=True)
    marker_order_in_category = models.IntegerField(choices=ORDER_FOR_CONCLUSION, null=True, blank=True)



    class Meta:
        verbose_name = 'Markers in Detection Kit'
        verbose_name_plural = 'Markers in Detection Kit'
        constraints = [models.UniqueConstraint(
                        fields=['detection_kit', 'marker', ],
                        name='detection_kit_marker_constraint')]

    def __str__(self):
        return f'detection kit: {self.detection_kit}, marker: {self.marker}'


    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        nuc_var_1 = self.marker.nuc_var_1
        nuc_var_2 = self.marker.nuc_var_2


        genotypes = [nuc_var_1 + nuc_var_1,
                    nuc_var_1 + nuc_var_2,
                    nuc_var_2 + nuc_var_2]


        for genotype in genotypes:
            ConclusionsForSNP.objects.create(
                det_kit_marker = self,
                genotype=genotype,

            )

    def clean(self):
        num_of_concs = ConclusionsForSNP.objects.filter(
            det_kit_marker=self.pk).all()
        if num_of_concs.count() == 3:
            raise ValidationError(
                'Conclusions for this marker already exists')




class ConclusionsForSNP(models.Model):
    det_kit_marker = models.ForeignKey(DetectionKitMarkers, on_delete=models.CASCADE)
    genotype = models.CharField(max_length=4)
    conclusion = models.TextField(max_length=2000, default=None, null=True, blank=True)

    class Meta:
        verbose_name ='conclusion for each SNP genotype'
        verbose_name_plural = '2. conclusions for each SNP genotype '

    @property
    def short_conclusion(self):
        return truncatewords(self.conclusion, 10)




