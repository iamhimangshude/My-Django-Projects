from django.db import models
import uuid, os


# Create your models here.
class Folder(models.Model):
    folder_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
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
    file_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.FileField(upload_to="files/")
    created_at = models.DateTimeField(auto_now_add=True)
    folder = models.ForeignKey(
        Folder,
        on_delete=models.CASCADE,
        related_name="files",
        null=True,
        blank=True,
    )

    def file_type(self):
        # Get the file extension
        _, extension = os.path.splitext(self.file.name)
        # Remove the dot from the extension
        extension = extension.lstrip(".")

        # Define mappings for common file types
        image_extensions = ["jpg", "jpeg", "png", "gif", "bmp"]
        document_extensions = [
            "pdf",
            "doc",
            "docx",
            "xls",
            "xlsx",
            "ppt",
            "pptx",
            "txt",
        ]
        video_extensions = ["mp4", "avi", "mkv", "mov", "wmv"]
        audio_extensions = ["mp3", "wav", "ogg", "flac"]

        # Check if the file extension belongs to a specific category
        if extension.lower() in image_extensions:
            return "image"
        elif extension.lower() in document_extensions:
            return "document"
        elif extension.lower() in video_extensions:
            return "video"
        elif extension.lower() in audio_extensions:
            return "audio"
        else:
            return "other"
