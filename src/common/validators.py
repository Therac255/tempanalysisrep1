import os

from django.core.exceptions import ValidationError


def validate_file_extension(value):
    valid_extensions = [".jpg", ".png", ".jpeg"]
    ext = os.path.splitext(value.name)[1].lower()
    if ext not in valid_extensions:
        raise ValidationError(
            f"Unsupported file extension. Supported extension includes: {valid_extensions}"
        )
