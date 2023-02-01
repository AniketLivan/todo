from rest_framework import generics, status
from rest_framework.response import Response
from .serializer import TaskSerializer
from django.contrib.auth.models import User
from .models import TaskModel
from datetime import datetime
import jwt
from jwtauthloginandregister.settings import SECRET_KEY

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

#Register API
class RegisterTask(generics.GenericAPIView):
    serializer_class = TaskSerializer

    def post(self, request, *args,  **kwargs):
        token = request.headers.get("authorization")
        authenticated = authenticate(token=token)
        if authenticated:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            task = serializer.save()
            return Response({
                "user": TaskSerializer(task, context=self.get_serializer_context()).data,
                "message": "User Created Successfully.  Now perform Login to get your token",
            })
        else:
            raise Exception("Invalid Token")


class TaskDetail(generics.GenericAPIView):
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer

    def get_task(self, pk):
        try:
            return TaskModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        token = request.headers.get("authorization")
        authenticated = authenticate(token=token)
        if authenticated:
            task = self.get_task(pk=pk)
            if task == None:
                return Response({"status": "fail", "message": f"task with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(task)
            return Response({"status": "success", "task": serializer.data})
        else:
            raise Exception("Invalid Token")

    def patch(self, request, pk):
        token = request.headers.get("authorization")
        authenticated = authenticate(token=token)
        if authenticated:
            task = self.get_task(pk)
            if task == None:
                return Response({"status": "fail", "message": f"task with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = self.serializer_class(
                task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data['updated_at'] = datetime.now()
                serializer.save()
                return Response({"status": "success", "task": serializer.data})
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Exception("Invalid Token")
             
            