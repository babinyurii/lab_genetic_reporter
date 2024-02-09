# Generated by Django 4.2.10 on 2024-02-09 07:27

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SingleNucPol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rs', models.CharField(max_length=20, unique=True, verbose_name='rs id')),
                ('gene_name_short', models.CharField(max_length=20, verbose_name='short gene name')),
                ('gene_name_full', models.CharField(blank=True, max_length=255, null=True, verbose_name='full gene name')),
                ('nuc_var_1', models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T')], max_length=1, verbose_name='allele 1')),
                ('nuc_var_2', models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T')], max_length=1, verbose_name='allele 2')),
                ('nuc_var_1_freq', models.FloatField(blank=True, help_text='floating point number. f.e.: 0.5', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='allele 1 frequency (from dbSNP)')),
                ('nuc_var_2_freq', models.FloatField(blank=True, help_text='floating point number. f.e.: 0.5', null=True, validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(1)], verbose_name='allele 2 frequency (from dbSNP)')),
                ('db_snp_link', models.URLField(blank=True, max_length=255, null=True, unique=True, validators=[django.core.validators.URLValidator], verbose_name='dbSNP link')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'SNP',
                'verbose_name_plural': 'SNPs',
            },
        ),
    ]
