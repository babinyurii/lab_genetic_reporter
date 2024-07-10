# Generated by Django 4.2.10 on 2024-03-11 13:09

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0008_alter_conclusionsnp_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientsample',
            name='age',
            field=models.PositiveIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(122)]),
        ),
    ]