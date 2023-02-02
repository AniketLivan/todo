from rest_framework import generics, status
from django.db import transaction
from rest_framework.response import Response
from .serializer import RegisterSerializer, UserSerializer
from django.contrib.auth.models import User
from task.models import TaskModel

#Register API
class RegisterApi(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    def post(self, request, *args,  **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({
            "user": UserSerializer(user,    context=self.get_serializer_context()).data,
            "message": "User Created Successfully.  Now perform Login to get your token",
        })

class RegisterAccountDetail(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def delete(self, request, pk):
        user = User.objects.get(pk=pk)
        if user == None:
            return Response({"status": "fail", "message": f"User with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
        try:
            with transaction.atomic():
                user.delete()
                tasks = TaskModel.objects.filter(created_by_id=pk)
                tasks.delete()
        except Exception:
            return Response({"status": "fail", "message": f"User with Id: {pk} not failed"}, status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)
