from rest_framework import  serializers
from .models import BookmarkModel

class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookmarkModel
        fields = '__all__'