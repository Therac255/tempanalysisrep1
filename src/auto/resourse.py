from import_export import fields, resources
from import_export.results import RowResult
from import_export.widgets import BooleanWidget, CharWidget, FloatWidget, ForeignKeyWidget, IntegerWidget

from auto.models import Car
from auto.models.body_type import BodyType
from auto.models.car_brand import CarBrand
from auto.models.car_color import CarColor
from auto.models.car_model import CarModel
from auto.models.country import Country
from auto.models.drive import Drive
from auto.models.engine_type import EngineType
from auto.models.engine_volume import EngineVolume
from auto.models.transmission import Transmission
from auto.widget import CaseInsensitiveForeignKeyWidget


class CarResource(resources.ModelResource):
    id = fields.Field(attribute='id')

    brand = fields.Field(
        column_name='Марка',
        attribute='brand',
        widget=CaseInsensitiveForeignKeyWidget(CarBrand, 'name')
    )
    model = fields.Field(
        column_name='Модель',
        attribute='model',
        widget=CaseInsensitiveForeignKeyWidget(CarModel, 'name')
    )
    body_type = fields.Field(
        column_name='Тип кузова',
        attribute='body_type',
        widget=CaseInsensitiveForeignKeyWidget(BodyType, 'name')
    )
    color = fields.Field(
        column_name='Цвет',
        attribute='color',
        widget=CaseInsensitiveForeignKeyWidget(CarColor, 'name')
    )
    engine_type = fields.Field(
        column_name='Тип двигателя',
        attribute='engine_type',
        widget=CaseInsensitiveForeignKeyWidget(EngineType, 'name')
    )
    engine_volume = fields.Field(
        column_name='Объем двигателя',
        attribute='engine_volume',
        widget=ForeignKeyWidget(EngineVolume, 'volume')
    )
    transmission_type = fields.Field(
        column_name='Тип КПП',
        attribute='transmission_type',
        widget=CaseInsensitiveForeignKeyWidget(Transmission, 'name')
    )
    drive_type = fields.Field(
        column_name='Привод',
        attribute='drive_type',
        widget=CaseInsensitiveForeignKeyWidget(Drive, 'name')
    )
    assembly_country = fields.Field(
        column_name='Страна сборки',
        attribute='assembly_country',
        widget=CaseInsensitiveForeignKeyWidget(Country, 'name')
    )
    manufacturing_year = fields.Field(column_name='Год выпуска', attribute='manufacturing_year')

    height = fields.Field(column_name='Высота (мм)', attribute='height', default=0, widget=FloatWidget())
    length = fields.Field(column_name='Длина (мм)', attribute='length', default=0, widget=FloatWidget())

    steering_side = fields.Field(
        column_name='Сторона руля',
        attribute='steering_side',
        default=0, widget=BooleanWidget())
    horsepower = fields.Field(
        column_name='Лошадиные силы',
        attribute='horsepower',
        default=0, widget=IntegerWidget())
    fuel_consumption = fields.Field(
        column_name='Расход топлива',
        attribute='fuel_consumption',
        default=0, widget=FloatWidget())
    acceleration = fields.Field(
        column_name='Разгон до 100 км/ч',
        attribute='acceleration',
        default=0, widget=FloatWidget())
    clearance = fields.Field(
        column_name='Дорожный просвет (мм)',
        attribute='clearance',
        default=0, widget=FloatWidget())
    wheelbase = fields.Field(
        column_name='Колесная база (мм)',
        attribute='wheelbase',
        default=0, widget=FloatWidget())
    front_track = fields.Field(
        column_name='Колея передняя (мм)',
        attribute='front_track',
        default=0, widget=FloatWidget())
    rear_track = fields.Field(
        column_name='Колея задняя (мм)',
        attribute='rear_track',
        default=0, widget=FloatWidget())
    front_tire_size = fields.Field(
        column_name='Размерность передних шин',
        attribute='front_tire_size',
        default='', widget=CharWidget(allow_blank=True))
    rear_tire_size = fields.Field(
        column_name='Размерность задних шин',
        attribute='rear_tire_size',
        default='', widget=CharWidget(allow_blank=True))
    engine_displacement = fields.Field(
        column_name='Рабочий объем двигателя (см куб)',
        attribute='engine_displacement',
        default=0, widget=IntegerWidget())
    num_of_cylinders = fields.Field(
        column_name='Количество цилиндров',
        attribute='num_of_cylinders',
        default=0, widget=IntegerWidget())
    front_brakes = fields.Field(
        column_name='Передние тормоза',
        attribute='front_brakes',
        default=0, widget=BooleanWidget())
    rear_brakes = fields.Field(
        column_name='Задние тормоза',
        attribute='rear_brakes',
        default=0, widget=BooleanWidget())
    num_of_doors = fields.Field(
        column_name='Количество дверей',
        attribute='num_of_doors',
        default=4, widget=IntegerWidget())
    euroNCAP_rating = fields.Field(
        column_name='Рейтинг EuroNCAP',
        attribute='euroNCAP_rating',
        default=0, widget=IntegerWidget())

    def import_row(self, row, instance_loader, **kwargs):
        # overriding import_row to ignore errors and skip rows that fail to import
        # without failing the entire import
        import_result = super(CarResource, self).import_row(row, instance_loader, **kwargs)
        if import_result.import_type == RowResult.IMPORT_TYPE_ERROR:
            import_result.diff = [row[val] for val in row]
            import_result.diff.append([str(err.error) for err in import_result.errors])
            import_result.errors = []
            import_result.import_type = RowResult.IMPORT_TYPE_SKIP

        return import_result

    class Meta:
        model = Car
        skip_unchanged = True
        report_skipped = True
        raise_errors = False

        use_bulk = False
        use_transactions = True
        collect_failed_rows = True
        use_natural_foreign_keys = False
        import_id_fields = (
            'brand',
            'model',
            'body_type',
            'color',
            'engine_type',
            'engine_volume',
            'transmission_type',
            'drive_type',
            'assembly_country',
            'manufacturing_year',
            'steering_side',
        )
        fields = (
            'brand',
            'model',
            'body_type',
            'color',
            'engine_type',
            'engine_volume',
            'transmission_type',
            'drive_type',
            'assembly_country',
            'manufacturing_year',
            'steering_side',
            'horsepower',
            'fuel_consumption',
            'acceleration',
            'length',
            'height',
            'clearance',
            'wheelbase',
            'front_track',
            'rear_track',
            'front_tire_size',
            'rear_tire_size',
            'engine_displacement',
            'num_of_cylinders',
            'front_brakes',
            'rear_brakes',
            'num_of_doors',
            'euroNCAP_rating',
        )
