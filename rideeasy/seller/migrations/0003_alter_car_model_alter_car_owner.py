# Generated by Django 5.0.6 on 2024-07-30 19:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('seller', '0002_car_model_car_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='car',
            name='model',
            field=models.CharField(default='default_model', max_length=50),
        ),
        migrations.AlterField(
            model_name='car',
            name='owner',
            field=models.CharField(default='default_owner', max_length=50),
        ),
    ]