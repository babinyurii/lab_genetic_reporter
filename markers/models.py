from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import URLValidator


def validate_rs(value):
    if not value.startswith('rs'):
        raise ValidationError(f'{value} should start with "rs"')

def validate_freq(value):
    if value >= 1 or value <= 0:
        raise ValidationError('frequency value should be in the range between 0 and 1')


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
    
    rs = models.CharField(max_length=20, verbose_name='Rs id', unique=True, validators=[validate_rs, ])
    gene_name_short = models.CharField(max_length=20, verbose_name='short gene name')
    gene_name_full = models.CharField(max_length=255, blank=True, null=True, verbose_name='full gene name')
    nuc_var_1 = models.CharField(max_length=1, choices=NUC_CHOICES, verbose_name='allele 1')
    nuc_var_2 = models.CharField(max_length=1, choices=NUC_CHOICES, verbose_name='allele 2')
    nuc_var_1_freq = models.FloatField(blank=True, null=True, verbose_name='allele 1 frequency (from dbSNP)',
                                        help_text='floating point number. f.e.: 0.5',
                                        validators=[validate_freq, ])
    nuc_var_2_freq = models.FloatField(blank=True, null=True, verbose_name='allele 2 frequency (from dbSNP)',
                                        help_text='floating point number. f.e.: 0.5',
                                        validators=[validate_freq, ])
    db_snp_link = models.URLField(max_length=255, blank=True, null=True, unique=True, verbose_name='dbSNP link',
                                    validators=[URLValidator, ])
    


    def clean(self):
        if self.nuc_var_1 == self.nuc_var_2:
            raise ValidationError('Allele 1 and allele 1 variants cannot be the same')
        if all([self.nuc_var_1_freq, self.nuc_var_2_freq]): 
            if sum([self.nuc_var_1_freq, self.nuc_var_2_freq]) != 1:
                raise ValidationError('allele frequency sum should be equal to 1')


    def __str__(self):
        return f'{self.rs} {self.gene_name_short} {self.nuc_var_1}/{self.nuc_var_2}'


    class Meta:
        verbose_name = 'SNP'
        verbose_name_plural = 'SNPs'
    