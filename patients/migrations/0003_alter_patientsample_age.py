# Generated by Django 4.2.10 on 2024-02-09 08:33

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientsample',
            name='age',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(122)]),
        ),
    ]