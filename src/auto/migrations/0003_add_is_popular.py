# Generated by Django 4.2.6 on 2023-11-01 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auto', '0002_init'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='car',
            options={'ordering': ['-vin_car__created'], 'verbose_name': 'Авто', 'verbose_name_plural': 'Авто'},
        ),
        migrations.AddField(
            model_name='carbrand',
            name='is_popular',
            field=models.BooleanField(default=False, verbose_name='Популярный'),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='is_popular',
            field=models.BooleanField(default=False, verbose_name='Популярный'),
        ),
    ]
