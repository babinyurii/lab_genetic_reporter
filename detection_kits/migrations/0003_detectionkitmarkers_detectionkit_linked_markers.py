# Generated by Django 4.2.10 on 2024-03-06 10:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markers', '0005_alter_singlenucpol_nuc_var_1_and_more'),
        ('detection_kits', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DetectionKitMarkers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detection_kit', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='detection_kits.detectionkit')),
                ('marker', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='markers.singlenucpol')),
            ],
        ),
        migrations.AddField(
            model_name='detectionkit',
            name='linked_markers',
            field=models.ManyToManyField(related_name='detection_kits_list', through='detection_kits.DetectionKitMarkers', to='markers.singlenucpol'),
        ),
    ]
