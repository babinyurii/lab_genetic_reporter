# Generated by Django 4.2.10 on 2024-03-12 10:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0009_alter_patientsample_age'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientsample',
            name='clinic_id',
            field=models.CharField(max_length=255, null=True),
        ),
    ]
