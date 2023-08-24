from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ActivityList(models.Model):
    title = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.title
    
    @property
    def status(self):
        items = self.items.all()
        progress = {item.status for item in items}
        if progress:
            if 'PE' not in progress:
                return 'Finished'
            if 'FI' not in progress:
                return 'Not Started'
            if 'IP' not in progress:
                return 'In Process'
            return 'En proceso'
        return 'Empty'
    
    @property
    def ietm_count(self):
        return self.items.count()

class ActivityItem(models.Model):
    class Progress(models.TextChoices):
        PENDING = 'PE', 'Pending'
        FINISHED = 'FI', 'Finished'
        IN_PROCESS = 'IP', 'In process'

    title = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    list_id = models.CharField(
        max_length=2,
        choices=Progress.choices,
        default=Progress.PENDING
    )

    def __str__(self):
        return self.title