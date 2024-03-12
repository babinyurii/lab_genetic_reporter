# Generated by Django 4.2.10 on 2024-03-12 10:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detection_kits', '0005_detectionkitmarkers_detection_kit_marker_constraint'),
        ('patients', '0010_alter_patientsample_clinic_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientsample',
            name='clinic_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='patientsampledetectionkit',
            name='patient_sample',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='patients.patientsample'),
        ),
        migrations.AlterField(
            model_name='patientsampledetectionkit',
            name='test',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='detection_kits.detectionkit'),
        ),
    ]
