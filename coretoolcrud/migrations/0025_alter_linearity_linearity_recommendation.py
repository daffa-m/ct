# Generated by Django 3.2.7 on 2022-03-21 08:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coretoolcrud', '0024_auto_20220321_0257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='linearity',
            name='linearity_recommendation',
            field=models.TextField(null=True),
        ),
    ]
