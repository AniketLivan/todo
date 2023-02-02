from datetime import datetime
from django.db import transaction
import math
from rest_framework import generics, status
from rest_framework.response import Response
from jwtauthloginandregister.settings import SECRET_KEY
from django.contrib.auth.models import User
from .models import CommentModel
from .serializer import CommentSerializer
from task.models import TaskModel
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

class RegisterComment(generics.GenericAPIView):
    serializer_class = CommentSerializer
    queryset = CommentModel.objects.all()

    def post(self, request, *args,  **kwargs):
        token = request.headers.get("authorization")
        authenticated = authenticate(token=token)
        if authenticated:
            
            data_to_add = {
                'created_by_id': authenticated['id'],
                'task_id': request.data.task_id,
                'description': request.data.description,
                'created_by_name': request.data.created_by_name
            }  
            serializer = self.serializer_class(data=data_to_add)
            try:
                with transaction.atomic():
                    serializer.save()
                    task = TaskModel.objects.filter(pk=request.data.task_id).select_for_update().get() 
                    task.validated_data["total_comments"] += 1
                    task.save()
            except Exception:
                return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "success", "comment": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            raise Exception("Invalid Token")

    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        comment = CommentModel.objects.filter(task_id=request.data.task_id).values_list('pk', flat=True)
        total_comment = comment.count()
        if search_param:
            comment = comment.filter(title__icontains=search_param)
        serializer = self.serializer_class(comment[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_comment,
            "page": page_num,
            "last_page": math.ceil(total_comment / limit_num),
            "comment": serializer.data
        })

class CommentDetail(generics.GenericAPIView):
    serializer_class = CommentSerializer
    queryset = CommentModel.objects.all()

    def get_comment(self, pk):
        try:
            return CommentModel.objects.get(pk=pk)
        except:
            return None

    def delete(self, request, id):
        token = request.headers.get("authorization")
        authenticated = authenticate(token=token)
        if authenticated:
            comment = self.get_comment(id)
            if comment == None:
                return Response({"status": "fail", "message": f"comment with Id: {id} not found"}, status=status.HTTP_404_NOT_FOUND)

            comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        comment = self.get_comment(pk)
        if comment == None:
            return Response({"status": "fail", "message": f"comment with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = self.serializer_class(
            comment, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.validated_data['updated_at'] = datetime.now()
            serializer.save()
            return Response({"status": "success", "comment": serializer.data})
        return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        comment = self.get_comment(pk)
        if comment == None:
            return Response({"status": "fail", "message": f"comment with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
