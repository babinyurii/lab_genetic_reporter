# Generated by Django 4.2.10 on 2024-02-15 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('patients', '0004_alter_patientsample_date_sampled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conclusionsnp',
            name='conclusion',
            field=models.TextField(max_length=20000),
        ),
        migrations.AlterField(
            model_name='reportcombinations',
            name='report',
            field=models.TextField(blank=True, max_length=10000, null=True),
        ),
    ]
