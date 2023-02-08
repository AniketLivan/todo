from django.db import models
from django.utils.translation import gettext_lazy as _
from jwtauthloginandregister import settings

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
    
    # id = models.IntegerField(primary_key=True)
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
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        permissions = (
            ('change_task_model', 'Change Taskmodel'),
        )
# Create your models here.

class BookmarkModel(models.Model):
    
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_id = models.ForeignKey('TaskModel', on_delete=models.CASCADE)
class CommentModel(models.Model):
    
    # id = models.IntegerField(primary_key=True)
    description = models.TextField()
    created_by_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    up_votes = models.IntegerField(default=0)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_id = models.ForeignKey('TaskModel', on_delete=models.CASCADE)

from django.db import models
from django.utils.translation import gettext_lazy as _
from jwtauthloginandregister import settings


# Create your models here.
class UserPermissionModel(models.Model):
    
    class Permission(models.TextChoices):
        read_only = 'RO', _('Read Only')
        edit = 'ED', _('Edit')

    # id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    assigned_to_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='%(class)s_requests_created')
    task_id = models.ForeignKey('TaskModel', on_delete=models.CASCADE)
    assigned_person = models.CharField(max_length=100)
    permission = models.CharField(max_length=3, choices=Permission.choices, default=Permission.read_only)



class VoteModel(models.Model):
    # id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_id = models.ForeignKey('TaskModel', on_delete=models.CASCADE)
    comment_id = models.ForeignKey('CommentModel', on_delete=models.CASCADE)
     

