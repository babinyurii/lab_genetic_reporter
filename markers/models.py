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
    
    rs = models.CharField(max_length=20, verbose_name='Rs id', unique=True)
    gene_name_short = models.CharField(max_length=20, verbose_name='short gene name')
    gene_name_full = models.CharField(max_length=255, blank=True, null=True, verbose_name='full gene name')
    nuc_var_1 = models.CharField(max_length=1, choices=NUC_CHOICES, verbose_name='allele 1')
    nuc_var_2 = models.CharField(max_length=1, choices=NUC_CHOICES, verbose_name='allele 2')
    nuc_var_1_freq = models.FloatField(blank=True, null=True, verbose_name='allele 1 frequency (from dbSNP)')
    nuc_var_2_freq = models.FloatField(blank=True, null=True, verbose_name='allele 2 frequency (from dbSNP)')
    db_snp_link = models.URLField(max_length=255, blank=True, null=True, unique=True, verbose_name='dbSNP link')


    def __str__(self):
        return f'{self.rs} {self.gene_name_short} {self.nuc_var_1}/{self.nuc_var_2}'


    class Meta:
        verbose_name = 'SNP'
        verbose_name_plural = 'SNPs'
    