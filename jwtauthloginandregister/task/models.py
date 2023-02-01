from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.
class TaskModel(models.Model):

    class Status(models.TextChoices):
        active = 'AC', _('Active')
        inactive = 'IAC', _('Inactive')
        deleted = 'DEL', _('Deleted')
    
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length = 200)
    description = models.TextField()
    assigned_to = models.CharField(max_length=200)
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.active)
    created_by_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_by_id = models.IntegerField()

