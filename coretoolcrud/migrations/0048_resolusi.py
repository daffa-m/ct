# Generated by Django 3.2.7 on 2022-08-27 14:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coretoolcrud', '0047_bias_bias_method'),
    ]

    operations = [
        migrations.CreateModel(
            name='Resolusi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('resolusi_survey_id', models.IntegerField()),
                ('resolusi_subgroup', models.IntegerField()),
                ('resolusi_nday', models.IntegerField()),
                ('resolusi_all', models.JSONField(null=True)),
                ('resolusi_reviewed', models.TextField()),
                ('resolusi_measured', models.TextField()),
                ('resolusi_unit', models.TextField()),
                ('resolusi_res', models.FloatField(null=True)),
            ],
        ),
    ]
