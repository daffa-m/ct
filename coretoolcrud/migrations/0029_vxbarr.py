# Generated by Django 3.2.7 on 2022-05-17 09:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coretoolcrud', '0028_remove_linearity_linearity_ave_reviewed'),
    ]

    operations = [
        migrations.CreateModel(
            name='Vxbarr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vxbarr_survey_id', models.IntegerField()),
                ('vxbarr_lsl', models.IntegerField()),
                ('vxbarr_usl', models.IntegerField()),
                ('vxbarr_subgroup', models.IntegerField()),
                ('vxbarr_unit', models.TextField()),
                ('vxbarr_all', models.JSONField(null=True)),
                ('vxbarr_measured', models.TextField()),
                ('vxbarr_reviewed', models.TextField()),
            ],
        ),
    ]