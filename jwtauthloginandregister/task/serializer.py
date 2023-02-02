from rest_framework import  serializers
from .models import TaskModel
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

# Register serializer
# class RegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = TaskModel
#         fields = ('id','title','description','assigned_to', 'status', 'created_by_name', 'created_at', 'updated_at', 'created_by_id')

#     def create(self, validated_data):
#         task = TaskModel.objects.create(validated_data['title'], description = validated_data['description'], assigned_to=validated_data['assigned_to'],  created_at=validated_data['created_at'], created_by_name=validated_data['created_by_name'], status=validated_data['status'], updated_at=validated_data['updated_at'], created_by_id=validated_data['created_by_id'])
#         return task
    
#     def update(self, validated_data, id):
#         task = TaskModel.objects.get(id=id)
#         if "description" in validated_data:
#             task.description = validated_data["description"]
#         if "assigned_to" in validated_data:
#             task.assigned_to = validated_data["assigned_to"]
#         if "status" in validated_data:
#             task.status = validated_data["status"]
#         if "title" in validated_data:
#             task.title = validated_data["title"]
#         task.save()
#         return "Updated"

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskModel
        fields = '__all__'