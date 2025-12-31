from django.db import models

# Create your models here.
import uuid
from django.db import models


class Paste(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    content = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    expires_at = models.DateTimeField(null=True, blank=True)
    max_views = models.PositiveIntegerField(null=True, blank=True)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return str(self.id)
    

