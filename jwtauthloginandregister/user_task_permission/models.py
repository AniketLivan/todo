from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class UserPermissionModel(models.Model):
    
    class Permission(models.TextChoices):
        read_only = 'RO', _('Read Only')
        edit = 'ED', _('Edit')

    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_id = models.IntegerField()
    updated_at = models.DateTimeField(auto_now_add=True)
    assigned_to_id = models.IntegerField()
    task_id = models.IntegerField()
    assigned_person = models.CharField(max_length=100)
    permission = models.CharField(max_length=3, choices=Permission.choices, default=Permission.read_only)