# Generated by Django 3.0.6 on 2020-05-25 00:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('home', '0002_auto_20180914_0302'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='service',
            options={'ordering': ('name',)},
        ),
        migrations.AlterField(
            model_name='service',
            name='sample_image',
            field=models.ImageField(blank=True, null=True, upload_to='home'),
        ),
        migrations.AlterField(
            model_name='service',
            name='serviceprovider',
            field=models.ManyToManyField(blank=True, null=True, to='home.ServiceProvider'),
        ),
        migrations.AlterField(
            model_name='serviceprovider',
            name='user',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='UserLocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('region', models.CharField(blank=True, max_length=250, null=True)),
                ('district', models.CharField(blank=True, max_length=250, null=True)),
                ('locality', models.CharField(blank=True, max_length=250, null=True)),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=20, null=True)),
                ('description', models.CharField(blank=True, max_length=200, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]