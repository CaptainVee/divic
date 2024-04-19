from django.core.exceptions import ValidationError
from django.db import models
import os

def validate_file_extension(value):

    ext = os.path.splitext(value.name)[1]  # [0] returns path+filename
    valid_extensions = ['.pdf', '.doc', '.docx']  # Define your valid extensions here
    if not ext.lower() in valid_extensions:
        raise ValidationError('Unsupported file extension.')

class Document(models.Model):
    file_name = models.CharField(max_length=250, null=True, blank=False)
    file = models.FileField(null=True, blank=True, validators=[validate_file_extension])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.file and not self.file_name:
            raise ValidationError("Either 'file' or 'file_name' must be provided.")
