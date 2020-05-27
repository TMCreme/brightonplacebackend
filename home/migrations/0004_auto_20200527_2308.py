# Generated by Django 3.0.6 on 2020-05-27 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_auto_20200525_0052'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='first_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='last_name',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location_latitude',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True),
        ),
        migrations.AddField(
            model_name='userprofile',
            name='location_longitude',
            field=models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='phone_number',
            field=models.CharField(blank=True, max_length=250, null=True),
        ),
    ]
