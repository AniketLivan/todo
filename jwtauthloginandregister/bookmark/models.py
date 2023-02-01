from django.db import models

# Create your models here.
class BookmarkModel(models.Model):
    
    id = models.IntegerField(primary_key=True)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by_id = models.IntegerField()
    task_id = models.IntegerField()