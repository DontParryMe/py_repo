import uuid
from django.db import models
from django.utils import timezone


class Robot(models.Model):
    serial = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    model = models.CharField(max_length=2, blank=False, null=False)
    version = models.CharField(max_length=2, blank=False, null=False)
    created = models.DateTimeField(default=timezone.now, blank=False, null=False)

