from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class ActivityList(models.Model):
    title = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    # owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def status(self):
        items = self.items.all()
        progress = {item.status for item in items}
        if progress:
            if 'PE' not in progress:
                return 'Finalizado'
            if 'FI' not in progress:
                return 'Pendiente'
            if 'IP' not in progress:
                return 'En proceso'
            return 'En proceso'
        return 'Vacio'
    
    @property
    def item_count(self):
        return self.items.count()

class ActivityItem(models.Model):
    class Progress(models.TextChoices):
        PENDING = 'PE', 'Pendiente'
        FINISHED = 'FI', 'Finalizado'
        IN_PROCESS = 'IP', 'En proceso'

    title = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    list_id = models.ForeignKey(ActivityList, on_delete=models.CASCADE, related_name='items')
    status = models.CharField(
        max_length=2,
        choices=Progress.choices,
        default=Progress.PENDING
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title