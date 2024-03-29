# Generated by Django 4.2.10 on 2024-02-09 07:27

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('detection_kits', '0001_initial'),
        ('markers', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ConclusionSNP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('conclusion', models.TextField(max_length=5000)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'conclusion for report',
                'verbose_name_plural': 'conclusions for reports',
            },
        ),
        migrations.CreateModel(
            name='PatientSample',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=255)),
                ('last_name', models.CharField(max_length=255)),
                ('middle_name', models.CharField(blank=True, max_length=255, null=True)),
                ('age', models.PositiveIntegerField()),
                ('clinic_id', models.CharField(blank=True, max_length=255, null=True)),
                ('lab_id', models.CharField(max_length=255, unique=True)),
                ('date_sampled', models.DateField(blank=True, null=True)),
                ('date_delivered', models.DateField()),
                ('dna_concentration', models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0)])),
                ('dna_quality_260_280', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(3.0)])),
                ('dna_quality_260_230', models.FloatField(validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(3.0)])),
                ('notes', models.TextField(blank=True, max_length=255, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
            ],
            options={
                'verbose_name': 'Sample',
                'verbose_name_plural': 'Samples',
            },
        ),
        migrations.CreateModel(
            name='ResultSNP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('result', models.CharField(blank=True, help_text='use only English characters for result', max_length=2, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('patient_sample', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patientsample')),
                ('rs', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='markers.singlenucpol')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detection_kits.detectionkit')),
            ],
            options={
                'verbose_name': 'SNP result',
                'verbose_name_plural': 'SNP results',
            },
        ),
        migrations.CreateModel(
            name='ReportRuleTwoSNP',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('note', models.TextField(max_length=1000)),
                ('order_in_conclusion', models.IntegerField(choices=[(1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6), (7, 7), (8, 8), (9, 9)], default=1)),
                ('snp_1', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_rules_snp_1', to='markers.singlenucpol')),
                ('snp_2', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_rules_snp_2', to='markers.singlenucpol')),
                ('tests', models.ManyToManyField(related_name='report_rules', to='detection_kits.detectionkit')),
            ],
        ),
        migrations.CreateModel(
            name='ReportCombinations',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genotype_snp_1', models.CharField(blank=True, max_length=2, null=True)),
                ('genotype_snp_2', models.CharField(blank=True, max_length=2, null=True)),
                ('report', models.TextField(blank=True, max_length=1000, null=True)),
                ('report_rule_two_snp', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.reportruletwosnp')),
            ],
            options={
                'verbose_name': 'report rules: conclusions for genotype combinations',
                'verbose_name_plural': 'report rules: conclusions for genotype combinations',
            },
        ),
        migrations.CreateModel(
            name='PatientSampleDetectionKit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('patient_sample', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patients.patientsample')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='detection_kits.detectionkit')),
            ],
            options={
                'verbose_name': 'Detection kit',
                'verbose_name_plural': 'Detection kits',
            },
        ),
    ]
