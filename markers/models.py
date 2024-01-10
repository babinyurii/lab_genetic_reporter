from django.db import models

class SingleNucPol(models.Model):
    ADENINE = 'A'
    CYTOSINE = 'C'
    GUANINE = 'G'
    THYMINE = 'T'

    NUC_CHOICES = (
        (ADENINE, 'A'),
        (CYTOSINE, 'C'),
        (GUANINE, 'G'),
        (THYMINE, 'T'),
    )
    
    rs = models.CharField(max_length=20)
    gene_name_short = models.CharField(max_length=20)
    gene_name_full = models.CharField(max_length=255, blank=True, null=True)
    nuc_var_1 = models.CharField(max_length=1, choices=NUC_CHOICES)
    nuc_var_2 = models.CharField(max_length=1, choices=NUC_CHOICES)
    nuc_var_1_freq = models.FloatField(blank=True, null=True)
    nuc_var_2_freq = models.FloatField(blank=True, null=True)
    db_snp_link = models.URLField(max_length=255, blank=True, null=True, unique=True)