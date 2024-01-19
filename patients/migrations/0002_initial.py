# Generated by Django 4.2.9 on 2024-01-19 09:22

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('patients', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('detection_kits', '0002_initial'),
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
    ]
