# Generated by Django 4.2.6 on 2023-11-06 17:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0003_add_is_popular'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='car',
            name='additional_services',
        ),
        migrations.AlterField(
            model_name='offer',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_offers', to='auto.car', verbose_name='Авто'),
        ),
    ]
