# Generated by Django 4.2.6 on 2023-10-31 11:03

import uuid

import ckeditor.fields
import django.core.validators
import django.db.models.deletion
from django.db import migrations, models

import common.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BodyType',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Тип кузова',
                'verbose_name_plural': 'Типы кузова',
                'db_table': 'body_type',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Car',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('manufacturing_year', models.PositiveIntegerField(verbose_name='Год выпуска')),
                ('horsepower', models.PositiveIntegerField(validators=[django.core.validators.MaxValueValidator(1000)], verbose_name='Лошадиные силы')),
                ('steering_side', models.BooleanField(default=True, verbose_name='Cторона руля (без галочки правый руль)')),
                ('fuel_consumption', models.FloatField(default=0.0, verbose_name='Расход топлива')),
                ('acceleration', models.FloatField(default=0.0, verbose_name='Разгон до 100 км/ч')),
                ('length', models.IntegerField(default=0, verbose_name='Длина (мм)')),
                ('height', models.IntegerField(default=0, verbose_name='Высота (мм)')),
                ('clearance', models.IntegerField(default=0, verbose_name='Дорожный просвет (мм)')),
                ('wheelbase', models.IntegerField(default=0, verbose_name='Колёсная база (мм)')),
                ('front_track', models.IntegerField(default=0, verbose_name='Колея передняя (мм)')),
                ('rear_track', models.IntegerField(default=0, verbose_name='Колея задняя (мм)')),
                ('front_tire_size', models.CharField(default=0, max_length=100, verbose_name='Размерность передних шин')),
                ('rear_tire_size', models.CharField(default=0, max_length=100, verbose_name='Размерность задних шин')),
                ('engine_displacement', models.IntegerField(default=0, verbose_name='Рабочий объем двигателя (см куб)')),
                ('num_of_cylinders', models.IntegerField(default=0, verbose_name='Количество цилиндров')),
                ('front_brakes', models.BooleanField(default=False, verbose_name='Передние тормоза')),
                ('rear_brakes', models.BooleanField(default=False, verbose_name='Задние тормоза')),
                ('num_of_doors', models.IntegerField(default=0, verbose_name='Количество дверей')),
                ('euroNCAP_rating', models.IntegerField(default=0, verbose_name='Рейтинг EuroNCAP')),
            ],
            options={
                'verbose_name': 'Авто',
                'verbose_name_plural': 'Авто',
                'db_table': 'car',
            },
        ),
        migrations.CreateModel(
            name='CarBrand',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('icon', models.FileField(upload_to='icons/', verbose_name='Иконка')),
            ],
            options={
                'verbose_name': 'Марка',
                'verbose_name_plural': 'Марки',
                'db_table': 'car_brand',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CarColor',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Цвет',
                'verbose_name_plural': 'Цвета',
                'db_table': 'car_color',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='CarImage',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('image', models.FileField(upload_to='cars/photos/', validators=[common.validators.validate_file_extension], verbose_name='Фото')),
            ],
            options={
                'verbose_name': 'Фото',
                'verbose_name_plural': 'Фото',
                'db_table': 'car_image',
            },
        ),
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Модель',
                'verbose_name_plural': 'Модели',
                'db_table': 'car_model',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Country',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Страна сборки',
                'verbose_name_plural': 'Страны сборки',
                'db_table': 'country',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Drive',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Привод',
                'verbose_name_plural': 'Привод',
                'db_table': 'drive',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EngineType',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Тип двигателя',
                'verbose_name_plural': 'Типы двигателей',
                'db_table': 'engine_type',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='EngineVolume',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('volume', models.FloatField(verbose_name='Объем')),
            ],
            options={
                'verbose_name': 'Объем двигателя',
                'verbose_name_plural': 'Объемы двигателей',
                'db_table': 'engine_volume',
            },
        ),
        migrations.CreateModel(
            name='Equipment',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Комплектация',
                'verbose_name_plural': 'Комплектации',
                'db_table': 'equipment',
            },
        ),
        migrations.CreateModel(
            name='Feature',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Функция',
                'verbose_name_plural': 'Функции',
                'db_table': 'feature',
            },
        ),
        migrations.CreateModel(
            name='Offer',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('description', ckeditor.fields.RichTextField(verbose_name='Описание от продавца')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='Стоимость')),
                ('discounted_price', models.PositiveIntegerField(blank=True, default=0, null=True, verbose_name='Стоимость со скидкой')),
                ('fuel_consumption', models.FloatField(default=0.0, verbose_name='Расход топлива')),
                ('acceleration', models.FloatField(default=0.0, verbose_name='Разгон до 100 км/ч')),
                ('length', models.IntegerField(default=0, verbose_name='Длина (мм)')),
                ('height', models.IntegerField(default=0, verbose_name='Высота (мм)')),
                ('clearance', models.IntegerField(default=0, verbose_name='Дорожный просвет (мм)')),
                ('wheelbase', models.IntegerField(default=0, verbose_name='Колёсная база (мм)')),
                ('front_track', models.IntegerField(default=0, verbose_name='Колея передняя (мм)')),
                ('rear_track', models.IntegerField(default=0, verbose_name='Колея задняя (мм)')),
                ('front_tire_size', models.CharField(default=0, max_length=100, verbose_name='Размерность передних шин')),
                ('rear_tire_size', models.CharField(default=0, max_length=100, verbose_name='Размерность задних шин')),
                ('engine_displacement', models.IntegerField(default=0, verbose_name='Рабочий объем двигателя (см куб)')),
                ('num_of_cylinders', models.IntegerField(default=0, verbose_name='Количество цилиндров')),
                ('front_brakes', models.BooleanField(default=False, verbose_name='Передние тормоза')),
                ('rear_brakes', models.BooleanField(default=False, verbose_name='Задние тормоза')),
                ('num_of_doors', models.IntegerField(default=0, verbose_name='Количество дверей')),
                ('euroNCAP_rating', models.IntegerField(default=0, verbose_name='Рейтинг EuroNCAP')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auto.car', verbose_name='Авто')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auto.equipment', verbose_name='Комплектация')),
            ],
            options={
                'verbose_name': 'Предложение',
                'verbose_name_plural': 'Предложения',
                'db_table': 'offer',
            },
        ),
        migrations.CreateModel(
            name='Transmission',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
            ],
            options={
                'verbose_name': 'Тип ККП',
                'verbose_name_plural': 'Типы ККП',
                'db_table': 'transmission',
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Vin',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('vin_code', models.CharField(max_length=17, verbose_name='Код VIN')),
                ('invoice', models.FileField(upload_to='invoice_files/', verbose_name='Инвойс')),
                ('packing_list', models.FileField(upload_to='packing_list_files/', verbose_name='Упаковочный лист')),
                ('CMR', models.FileField(upload_to='cmr_files/', verbose_name='CMR')),
                ('customs_inspection_report', models.FileField(upload_to='customs_inspection_report_files/', verbose_name='Акт таможенного осмотра')),
                ('seller_proxy_to_broker', models.FileField(upload_to='seller_proxy_to_broker_files/', verbose_name='Доверенность продавца на брокера')),
                ('handover_act', models.FileField(upload_to='handover_act_files/', verbose_name='Акт приема - передачи')),
                ('contract', models.FileField(upload_to='contract_files/', verbose_name='Договор')),
                ('status', models.CharField(choices=[('needs_moderation', 'Требует модерации'), ('moderated', 'Промодерирован на СВХ'), ('reserved', 'Забронирован'), ('paid', 'Оплачен'), ('in_transit', 'В пути'), ('ready', 'Готов к выдаче')], default='needs_moderation', max_length=30, verbose_name='Статус')),
                ('fuel_consumption', models.FloatField(default=0.0, verbose_name='Расход топлива')),
                ('acceleration', models.FloatField(default=0.0, verbose_name='Разгон до 100 км/ч')),
                ('length', models.IntegerField(default=0, verbose_name='Длина (мм)')),
                ('height', models.IntegerField(default=0, verbose_name='Высота (мм)')),
                ('clearance', models.IntegerField(default=0, verbose_name='Дорожный просвет (мм)')),
                ('wheelbase', models.IntegerField(default=0, verbose_name='Колёсная база (мм)')),
                ('front_track', models.IntegerField(default=0, verbose_name='Колея передняя (мм)')),
                ('rear_track', models.IntegerField(default=0, verbose_name='Колея задняя (мм)')),
                ('front_tire_size', models.CharField(default=0, max_length=100, verbose_name='Размерность передних шин')),
                ('rear_tire_size', models.CharField(default=0, max_length=100, verbose_name='Размерность задних шин')),
                ('engine_displacement', models.IntegerField(default=0, verbose_name='Рабочий объем двигателя (см куб)')),
                ('num_of_cylinders', models.IntegerField(default=0, verbose_name='Количество цилиндров')),
                ('front_brakes', models.BooleanField(default=False, verbose_name='Передние тормоза')),
                ('rear_brakes', models.BooleanField(default=False, verbose_name='Задние тормоза')),
                ('num_of_doors', models.IntegerField(default=0, verbose_name='Количество дверей')),
                ('euroNCAP_rating', models.IntegerField(default=0, verbose_name='Рейтинг EuroNCAP')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vin_car', to='auto.car', verbose_name='Авто')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vin_equipment', to='auto.equipment', verbose_name='Комплектация')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='vin_offer', to='auto.offer', verbose_name='Предложение')),
            ],
            options={
                'verbose_name': 'VIN',
                'verbose_name_plural': 'VIN',
                'db_table': 'vin',
            },
        ),
        migrations.CreateModel(
            name='TransportInvoiceDocument',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('file', models.FileField(upload_to='transport_invoice_documents/', verbose_name='Товарно-транспортная накладная')),
                ('vin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transport_invoice_documents', to='auto.vin')),
            ],
            options={
                'verbose_name': 'Товарно-транспортная накладная',
                'verbose_name_plural': 'Товарно-транспортные накладные',
                'db_table': 'transport_invoice_document',
            },
        ),
        migrations.CreateModel(
            name='TransitDeclarationDocument',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('document', models.FileField(upload_to='transit_declaration_documents/', verbose_name='Документы транзитной декларации')),
                ('vin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='transit_declaration_documents', to='auto.vin')),
            ],
            options={
                'verbose_name': 'Документ транзитной декларации',
                'verbose_name_plural': 'Документы транзитной декларации',
                'db_table': 'transit_declaration_document',
            },
        ),
        migrations.CreateModel(
            name='TechnicalImage',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('image', models.FileField(upload_to='car_ad_images/', validators=[common.validators.validate_file_extension], verbose_name='Технические фотографии')),
                ('vin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_ad_images', to='auto.vin')),
            ],
            options={
                'verbose_name': 'Техническое фото объявления',
                'verbose_name_plural': 'Технические фото объявления',
                'db_table': 'technical_image',
            },
        ),
        migrations.CreateModel(
            name='Subsection',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Имя')),
                ('equipment', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subsections', to='auto.equipment', verbose_name='Комплектация')),
            ],
            options={
                'verbose_name': 'Подраздел',
                'verbose_name_plural': 'Подразделы',
                'db_table': 'subsection',
            },
        ),
        migrations.CreateModel(
            name='ProductDeclarationDocument',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('file', models.FileField(upload_to='product_declaration_documents/', verbose_name='Декларация на товары')),
                ('vin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_declaration_documents', to='auto.vin')),
            ],
            options={
                'verbose_name': 'Декларация на товары',
                'verbose_name_plural': 'Декларация на товары',
                'db_table': 'product_declaration_document',
            },
        ),
        migrations.CreateModel(
            name='OfferImage',
            fields=[
                ('created', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('modified', models.DateTimeField(blank=True, db_index=True, null=True)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True, verbose_name='ID')),
                ('image', models.FileField(upload_to='offer_images/', verbose_name='Фотографии от продавца')),
                ('offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offer_images', to='auto.offer')),
            ],
            options={
                'verbose_name': 'Фотография предложения',
                'verbose_name_plural': 'Фотографии предложений',
                'db_table': 'offer_image',
            },
        ),
    ]
