# Generated by Django 4.2.9 on 2024-01-18 12:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('detection_kits', '0002_initial'),
        ('patients', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PatientSampleDetectionKit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rs', models.CharField(blank=True, max_length=20, null=True)),
                ('rs_result', models.CharField(blank=True, max_length=2, null=True)),
                ('patient_sample', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='patients.patientsample')),
                ('test', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='detection_kits.detectionkit')),
            ],
        ),
        migrations.AddField(
            model_name='patientsample',
            name='tests',
            field=models.ManyToManyField(through='patients.PatientSampleDetectionKit', to='detection_kits.detectionkit'),
        ),
    ]
