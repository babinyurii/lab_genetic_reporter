from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import (URLValidator,
                                    MinValueValidator,
                                    MaxValueValidator,)
from users.models import CustomUser
from markers.constants import NUC_CHOICES, ALLELE_CLIN_SIGNIF_CHOICE

class SingleNucPol(models.Model):
    

    rs = models.CharField(max_length=20, verbose_name='rs id', unique=True)
    gene_name_short = models.CharField(max_length=20,
                                       verbose_name='short gene name')
    gene_name_full = models.CharField(max_length=255,
                                      blank=True, null=True,
                                      verbose_name='full gene name')
    nuc_var_1 = models.CharField(max_length=2, choices=NUC_CHOICES,
                                 verbose_name='allele 1')
    nuc_var_1_clin_signif = models.CharField(
                                choices=ALLELE_CLIN_SIGNIF_CHOICE,
                                max_length=7,
                                blank=True,
                                null=True,
                                default=ALLELE_CLIN_SIGNIF_CHOICE[2][1],
                                verbose_name='allele 1 clinical significance'
                                )
    nuc_var_2 = models.CharField(max_length=2, choices=NUC_CHOICES,
                                 verbose_name='allele 2')
    nuc_var_2_clin_signif = models.CharField(
                                choices=ALLELE_CLIN_SIGNIF_CHOICE,
                                max_length=7, blank=True, null=True,
                                default=ALLELE_CLIN_SIGNIF_CHOICE[2][1],
                                verbose_name='allele 2 clinical significance'
                                )
    nuc_var_1_freq = models.FloatField(
                                blank=True, null=True,
                                verbose_name='allele 1 frequency (from dbSNP)',
                                help_text='floating point number. f.e.: 0.5',
                                validators=[MinValueValidator(0),
                                MaxValueValidator(1),]
                                )
    nuc_var_2_freq = models.FloatField(
                                blank=True, null=True,
                                verbose_name='allele 2 frequency (from dbSNP)',
                                help_text='floating point number. f.e.: 0.5',
                                validators=[MinValueValidator(0),
                                MaxValueValidator(1),]
                                )
    db_snp_link = models.URLField(max_length=255, blank=True,
                                  null=True, unique=True,
                                  verbose_name='dbSNP link',
                                  validators=[URLValidator, ],
                                  help_text=('LINK WILL BE OPENED'
                                             'IN THE SAME TAB! BE CAREFUL')
                                  )
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    date_modified = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(CustomUser, null=True,
                                blank=True, on_delete=models.PROTECT)

    def clean(self):
        if self.nuc_var_1 == self.nuc_var_2:
            raise ValidationError(
                'Allele 1 and allele 1 variants cannot be the same')
        if all([self.nuc_var_1_freq, self.nuc_var_2_freq]):
            if sum([self.nuc_var_1_freq, self.nuc_var_2_freq]) != 1:
                raise ValidationError(
                    'allele frequency sum should be equal to 1')
        if not self.rs.startswith('rs'):
            raise ValidationError(
                f'{self.rs} should start with "rs"')
        if not self.rs[2:].isnumeric():
            raise ValidationError(
                'rs id field should contain only numbers after "rs"')

    def __str__(self):
        return f'{self.rs} {self.gene_name_short} \
            {self.nuc_var_1}/{self.nuc_var_2}'

    class Meta:
        verbose_name = 'SNP'
        verbose_name_plural = 'SNPs'
