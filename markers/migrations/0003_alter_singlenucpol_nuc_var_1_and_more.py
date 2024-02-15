# Generated by Django 4.2.10 on 2024-02-15 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('markers', '0002_alter_singlenucpol_nuc_var_1_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='singlenucpol',
            name='nuc_var_1',
            field=models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T'), ('5A', '5A'), ('6A', '6A'), ('_', '-')], max_length=2, verbose_name='allele 1'),
        ),
        migrations.AlterField(
            model_name='singlenucpol',
            name='nuc_var_2',
            field=models.CharField(choices=[('A', 'A'), ('C', 'C'), ('G', 'G'), ('T', 'T'), ('5A', '5A'), ('6A', '6A'), ('_', '-')], max_length=2, verbose_name='allele 2'),
        ),
    ]
