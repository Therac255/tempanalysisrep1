# Generated by Django 4.2.6 on 2023-10-31 11:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('seller', '0001_init'),
        ('orders', '0001_init'),
        ('auto', '0001_init'),
    ]

    operations = [
        migrations.AddField(
            model_name='offer',
            name='seller',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='seller.seller', verbose_name='Продавец'),
        ),
        migrations.AddField(
            model_name='feature',
            name='subsection',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='features', to='auto.subsection', verbose_name='Подраздел'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auto.carbrand', verbose_name='Марка'),
        ),
        migrations.AddField(
            model_name='equipment',
            name='model',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auto.carmodel', verbose_name='Модель'),
        ),
        migrations.AddField(
            model_name='carmodel',
            name='brand',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cars_brand_model', to='auto.carbrand', verbose_name='Марка'),
        ),
        migrations.AddField(
            model_name='carimage',
            name='car',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='car_images', to='auto.car'),
        ),
        migrations.AddField(
            model_name='car',
            name='additional_services',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='orders.additionalservices', verbose_name='Доп услуги'),
        ),
        migrations.AddField(
            model_name='car',
            name='assembly_country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars_assembly_country', to='auto.country', verbose_name='Страна сборки'),
        ),
        migrations.AddField(
            model_name='car',
            name='body_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars_body_type', to='auto.bodytype', verbose_name='Тип кузова'),
        ),
        migrations.AddField(
            model_name='car',
            name='brand',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars_brand', to='auto.carbrand', verbose_name='Марка'),
        ),
        migrations.AddField(
            model_name='car',
            name='color',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars_color', to='auto.carcolor', verbose_name='Цвет'),
        ),
        migrations.AddField(
            model_name='car',
            name='drive_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars_drive_type', to='auto.drive', verbose_name='Привод'),
        ),
        migrations.AddField(
            model_name='car',
            name='engine_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars_engine_type', to='auto.enginetype', verbose_name='Тип двигателя'),
        ),
        migrations.AddField(
            model_name='car',
            name='engine_volume',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars_engine_volume', to='auto.enginevolume', verbose_name='Объем двигателя'),
        ),
        migrations.AddField(
            model_name='car',
            name='model',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars_model', to='auto.carmodel', verbose_name='Модель'),
        ),
        migrations.AddField(
            model_name='car',
            name='transmission_type',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='cars_transmission_type', to='auto.transmission', verbose_name='Тип ККП'),
        ),
        migrations.AlterUniqueTogether(
            name='offer',
            unique_together={('seller', 'car', 'equipment')},
        ),
        migrations.AddConstraint(
            model_name='car',
            constraint=models.UniqueConstraint(fields=('brand', 'model', 'body_type', 'color', 'engine_type', 'engine_volume', 'transmission_type', 'drive_type', 'assembly_country', 'manufacturing_year', 'steering_side'), name='unique_car'),
        ),
    ]
