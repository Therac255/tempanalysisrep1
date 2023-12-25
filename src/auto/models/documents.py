
# from django.utils.translation import gettext_lazy as _
# from django.db import models

# from app.models import TimestampedModel


# def generate_path(instance, filename):
#     return f"{instance.type}_files/{filename}"


# class VINDocumentModel(TimestampedModel):
#     class Meta:
#         db_table = "vin_documents"
#         verbose_name = _("Документ")
#         verbose_name_plural = _("Документы")
    
    
#     vin = models.ForeignKey(
#         "auto.VIN",
#         on_delete=models.CASCADE,
#         related_name="documents"
#     )
#     file = models.FileField(
#         upload_to=generate_path
#     )
#     type = models.CharField()