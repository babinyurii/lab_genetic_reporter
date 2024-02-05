# Generated by Django 4.2.9 on 2024-02-05 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('markers', '0001_initial'),
        ('patients', '0004_alter_reportruletwosnp_note_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reportruletwosnp',
            name='snp_1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_rules_snp_1', to='markers.singlenucpol'),
        ),
        migrations.AlterField(
            model_name='reportruletwosnp',
            name='snp_2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='report_rules_snp_2', to='markers.singlenucpol'),
        ),
    ]
