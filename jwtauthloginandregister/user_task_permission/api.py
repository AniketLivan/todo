from datetime import datetime
import math
from rest_framework import generics, status
from rest_framework.response import Response
from jwtauthloginandregister.settings import SECRET_KEY
from django.contrib.auth.models import User
from .models import UserPermissionModel
from .serializer import UserPermissionSerializer
import jwt

def authenticate(token):
    try:
        payload = jwt.decode(jwt=token, key=SECRET_KEY, algorithms=['HS256'])
        if "id" in payload:
            user = User.objects.get(token=payload["id"])
        else:
            return None
    except User.Doestaskxist:
        return None

    if not user.is_active:
        return None

    return user

class RegisterPermission(generics.GenericAPIView):
    serializer_class = UserPermissionSerializer
    queryset = UserPermissionModel.objects.all()

    def post(self, request, *args,  **kwargs):
        token = request.headers.get("authorization")
        authenticated = authenticate(token=token)
        if authenticated:
            if 'user' in request.data:
                
                data_to_add = {
                    'created_by_id': authenticated['id'],
                    'assigned_to_id': request.data.user.id,
                    'task_id': request.data.task_id,
                    'assigned_person': request.data.user['name'],
                    'permission': request.data.user['permission']
                }  
                serializer = self.serializer_class(data=data_to_add)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "permission": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Exception("Invalid Token")

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        permission = UserPermissionModel.objects.all()
        total_permission = permission.count()
        if search_param:
            permission = permission.filter(title__icontains=search_param)
        serializer = self.serializer_class(permission[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_permission,
            "page": page_num,
            "last_page": math.ceil(total_permission / limit_num),
            "permission": serializer.data
        })

class PermissionDetail(generics.GenericAPIView):
    serializer_class = UserPermissionSerializer
    queryset = UserPermissionModel.objects.all()

    def get_permission(self, pk):
        try:
            return UserPermissionModel.objects.get(pk=pk)
        except:
            return None

    def delete(self, request, id):
        token = request.headers.get("authorization")
        authenticated = authenticate(token=token)
        if authenticated:
            Permission = self.get_permission(id)
            if Permission == None:
                return Response({"status": "fail", "message": f"Permission with Id: {id} not found"}, status=status.HTTP_404_NOT_FOUND)

            Permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        permission = self.get_permission(pk)
        if permission == None:
            return Response({"status": "fail", "message": f"permission with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            permission, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updated_at'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "permission": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
