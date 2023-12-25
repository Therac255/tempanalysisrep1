from import_export.widgets import ForeignKeyWidget


class CaseInsensitiveForeignKeyWidget(ForeignKeyWidget):
    """
    Custom case-insensitive widget for ForeignKey.
    """

    def get_queryset(self, value, row, *args, **kwargs):
        return self.model.objects.filter(
            name__iexact=value
        )

    def clean(self, value, row=None, **kwargs):
        obj = self.get_queryset(value, row, **kwargs).first()
        if obj:
            return obj
        raise ValueError(
            f'Значение "{value}" не найдено в справочниках. Убедитесь в точности введённых данных в колонке "{self.model._meta.verbose_name.title()}"')
