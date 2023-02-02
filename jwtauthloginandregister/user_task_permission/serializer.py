from .models import UserPermissionModel
from rest_framework import  serializers


class UserPermissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserPermissionModel
        fields = '__all__'