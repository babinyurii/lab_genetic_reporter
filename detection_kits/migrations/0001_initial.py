# Generated by Django 4.2.10 on 2024-02-09 07:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DetectionKit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
                ('date_created', models.DateTimeField(auto_now_add=True)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('kit_type', models.CharField(choices=[('SNP', 'in-house SNP assay')], default='SNP', max_length=20)),
            ],
            options={
                'verbose_name': 'SNP detection kit',
                'verbose_name_plural': 'SNP detection kits',
            },
        ),
    ]
