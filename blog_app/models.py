from django.db import models
from django.core.validators import MinLengthValidator
import uuid

from auth_app.models import UserModel 

# Create your models here.

class Post(models.Model):
    post_id = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    title = models.CharField(max_length=255)
    excerpt = models.CharField(max_length=300)
    content = models.TextField(verbose_name='Post Content', validators=[MinLengthValidator(10)])
    image = models.ImageField(upload_to='images/')
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='posts')

    def __str__(self):
        return self.title

    def get_creator(self):
        return self.creator.first_name + ' ' + self.creator.last_name
