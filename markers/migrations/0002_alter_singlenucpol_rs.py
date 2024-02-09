# Generated by Django 4.2.10 on 2024-02-09 06:41

from django.db import migrations, models
import markers.models


class Migration(migrations.Migration):

    dependencies = [
        ('markers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlenucpol',
            name='rs',
            field=models.CharField(max_length=20, unique=True, validators=[markers.models.validate_rs], verbose_name='rs id'),
        ),
    ]
