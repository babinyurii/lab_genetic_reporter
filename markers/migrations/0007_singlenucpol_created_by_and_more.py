# Generated by Django 4.2.10 on 2024-03-11 11:25

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('markers', '0006_singlenucpol_nuc_var_1_clin_signif_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='singlenucpol',
            name='created_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='singlenucpol',
            name='db_snp_link',
            field=models.URLField(blank=True, help_text='LINK WILL BE OPENEDIN THE SAME TAB! BE CAREFUL', max_length=255, null=True, unique=True, validators=[django.core.validators.URLValidator], verbose_name='dbSNP link'),
        ),
    ]
