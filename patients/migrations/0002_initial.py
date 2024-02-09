# Generated by Django 4.2.10 on 2024-02-09 07:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
        ('detection_kits', '0002_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='patientsample',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='patientsample',
            name='tests',
            field=models.ManyToManyField(through='patients.PatientSampleDetectionKit', to='detection_kits.detectionkit'),
        ),
        migrations.AddField(
            model_name='conclusionsnp',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patientsample'),
        ),
        migrations.AddField(
            model_name='conclusionsnp',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detection_kits.detectionkit'),
        ),
        migrations.AddConstraint(
            model_name='patientsampledetectionkit',
            constraint=models.UniqueConstraint(fields=('patient_sample', 'test'), name='patient_and_test_unique_constraint'),
        ),
        migrations.AddConstraint(
            model_name='conclusionsnp',
            constraint=models.UniqueConstraint(fields=('patient', 'test'), name='patient_and_test_unique_constraint_for_conclusion'),
        ),
    ]
