from rest_framework import permissions
import jwt
from django.contrib.auth.models import User

from jwtauthloginandregister.settings import SECRET_KEY



class AllButTaskCreatorGetReadOnly(permissions.BasePermission):

    edit_methods = ("PUT", "PATCH")
    def has_permission(self, request, view):
        try:
            payload = jwt.decode(jwt=request.headers.authoriztation, key=SECRET_KEY, algorithms=['HS256'])
            user = User.objects.get(token=payload["id"])
            if not user:
                return False
        except Exception:
            return False
        return True

    def has_object_permission(self, request, view, obj):
        payload = jwt.decode(jwt=request.headers.authoriztation, key=SECRET_KEY, algorithms=['HS256'])
        
        if request.user.is_superuser:
            return True

        if request.method in permissions.SAFE_METHODS:
            return True

        if obj.created_by_id == payload["id"]:
            return True

        return False