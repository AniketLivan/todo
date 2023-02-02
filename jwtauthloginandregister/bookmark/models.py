from django.db import models
from jwtauthloginandregister import settings
# Create your models here.
class BookmarkModel(models.Model):
    
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    task_id = models.ForeignKey('task.TaskModel', on_delete=models.CASCADE)