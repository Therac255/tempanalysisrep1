from django.db import models
from django.utils.translation import gettext_lazy as _

from app.models import TimestampedModel


class NamedBaseModel(TimestampedModel):
    """
    This class is an abstract base model that serves as the base for models that have a 'name' field.

    Attributes:
        name (CharField): A character field that represents the name of the model.
    """

    name = models.CharField(verbose_name=_("Имя"), max_length=255)

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        verbose_name = ""
        verbose_name_plural = ""
