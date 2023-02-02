from django.db import models

# Create your models here.
class CommentModel(models.Model):
    
    id = models.IntegerField(primary_key=True)
    description = models.TextField()
    created_by_name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    up_votes = models.IntegerField(default=0)
    created_by_id = models.IntegerField()
    task_id = models.IntegerField()

