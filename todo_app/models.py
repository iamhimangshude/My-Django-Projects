from django.db import models
import uuid

# Create your models here.


class Category(models.Model):
    cat_name = models.CharField(unique=True, max_length=31)

    def __str__(self):
        return self.cat_name


class Tasks(models.Model):
    task_id = models.UUIDField(primary_key=True, editable=False, default=uuid.uuid4)
    title = models.CharField(max_length=100)
    detail_text = models.TextField(blank=True)
    due_date = models.DateField(blank=True, null=True)
    is_starred = models.BooleanField(default=False)
    is_completed = models.BooleanField(default=False)
    cat_name = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="category"
    )

    def __str__(self):
        return self.title
