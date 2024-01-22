# Generated by Django 4.2.9 on 2024-01-22 12:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markers', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='singlenucpol',
            options={'verbose_name': 'SNP', 'verbose_name_plural': 'SNPs'},
        ),
        migrations.AlterField(
            model_name='singlenucpol',
            name='db_snp_link',
            field=models.URLField(blank=True, max_length=255, null=True, unique=True, verbose_name='dbSNP link'),
        ),
        migrations.AlterField(
            model_name='singlenucpol',
            name='gene_name_full',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='full gene name'),
        ),
        migrations.AlterField(
            model_name='singlenucpol',
            name='gene_name_short',
            field=models.CharField(max_length=20, verbose_name='short gene name'),
        ),
        migrations.AlterField(
            model_name='singlenucpol',
            name='nuc_var_1',
            field=models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T')], max_length=1, verbose_name='allele 1'),
        ),
        migrations.AlterField(
            model_name='singlenucpol',
            name='nuc_var_1_freq',
            field=models.FloatField(blank=True, null=True, verbose_name='allele 1 frequency (from dbSNP)'),
        ),
        migrations.AlterField(
            model_name='singlenucpol',
            name='nuc_var_2',
            field=models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T')], max_length=1, verbose_name='allele 2'),
        ),
        migrations.AlterField(
            model_name='singlenucpol',
            name='nuc_var_2_freq',
            field=models.FloatField(blank=True, null=True, verbose_name='allele 2 frequency (from dbSNP)'),
        ),
        migrations.AlterField(
            model_name='singlenucpol',
            name='rs',
            field=models.CharField(max_length=20, unique=True, verbose_name='Rs id'),
        ),
    ]
