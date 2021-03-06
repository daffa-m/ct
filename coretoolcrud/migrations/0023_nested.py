# Generated by Django 3.2.7 on 2022-03-09 02:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coretoolcrud', '0022_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Nested',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nested_survey_id', models.IntegerField()),
                ('nested_nkaryawan', models.IntegerField()),
                ('nested_npart', models.IntegerField()),
                ('nested_ntrial', models.IntegerField()),
                ('nested_stdev', models.FloatField()),
                ('nested_stdevmax', models.FloatField()),
                ('nested_stdevmin', models.FloatField()),
                ('nested_karyawan', models.JSONField(null=True)),
                ('nested_all', models.JSONField(null=True)),
                ('nested_resume', models.JSONField(null=True)),
                ('nested_psvc', models.TextField(null=True)),
                ('nested_rva', models.TextField(null=True)),
                ('nested_xva', models.TextField(null=True)),
                ('nested_dbs', models.TextField(null=True)),
                ('nested_dba', models.TextField(null=True)),
                ('nested_aabp', models.TextField(null=True)),
                ('nested_recommendation', models.JSONField(null=True)),
            ],
        ),
    ]
