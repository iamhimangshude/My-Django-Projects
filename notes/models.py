from django.db import models

# Create your models here.
class Notes(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.title == "" and self.content != "":
            self.title = self.content[:12]
            super().save(*args, **kwargs)
        
        elif self.content == "" and self.title != "": 
            super().save(*args, **kwargs)

        elif self.title != "" and self.content != "":
            super().save(*args, **kwargs)
        else:
            pass
    
    class Meta:
        verbose_name_plural = "Notes"