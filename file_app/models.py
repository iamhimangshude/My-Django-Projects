from django.db import models


# Create your models here.
class Folder(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    is_subfolder = models.BooleanField(default=False)
    parent_folder = models.ForeignKey(
        "self",
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name="subfolders",
    )


class File(models.Model):
    file = models.FileField(upload_to="files")
    created_at = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="files",
        null=True,
        blank=True,
    )
