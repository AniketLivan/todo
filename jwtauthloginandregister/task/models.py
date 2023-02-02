from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

# class Permission(models.TextChoices):
#     read_only = 'RO', _('Read Only')
#     edit = 'ED', _('Edit')
# class AssignedToPermissions(models.Model):
#     id = models.IntegerField()
#     name = models.CharField(max_length=200)
#     permission = models.CharField(max_length=2, choices=Permission.choices, default=Permission.read_only)
#     class Meta:
#         abstract = True

# class AssignedToPermissionsForm(forms.ModelForm):
#     class Meta:
#         model = AssignedToPermissions
#         fields = (
#             'id','name', 'permission'
#         )
class TaskModel(models.Model):
    class Status(models.TextChoices):
        active = 'AC', _('Active')
        inactive = 'IAC', _('Inactive')
        deleted = 'DEL', _('Deleted')
    
    id = models.IntegerField(primary_key=True)
    title = models.CharField(max_length = 200)
    description = models.TextField()
    # assigned_to = models.ArrayField(
    #     model_container=AssignedToPermissions,
    #     model_form_class=AssignedToPermissionsForm
    # )
    status = models.CharField(max_length=3, choices=Status.choices, default=Status.active)
    created_by_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    total_comments = models.IntegerField(default=0)
    created_by_id = models.IntegerField()

