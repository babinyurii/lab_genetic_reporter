# Generated by Django 4.2.10 on 2024-03-06 10:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('detection_kits', '0003_detectionkitmarkers_detectionkit_linked_markers'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='detectionkit',
            name='markers',
        ),
    ]