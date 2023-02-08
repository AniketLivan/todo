import math
from rest_framework import generics, status
from rest_framework.response import Response
from .serializer import TaskSerializer, UserSerializer, RegisterSerializer, BookmarkSerializer, CommentSerializer, UserPermissionSerializer, VoteSerializer
from django.contrib.auth.models import User
from .models import TaskModel, BookmarkModel, CommentModel, UserPermissionModel, VoteModel
from datetime import datetime
import jwt
from jwtauthloginandregister.settings import SECRET_KEY
from guardian.shortcuts import assign_perm
from django.db import transaction
 

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
        # token = request.headers.get("authorization")
        # request.user.is_authenticated = authenticate(token=token)
        if request.user.is_authenticated:
            data = request.data
            data['created_by'] = request.user.id
            serializer = self.get_serializer(data=data)
            serializer.is_valid(raise_exception=True)
            task = serializer.save()
            assign_perm('task.change_task_model', request.user, task)
            return Response({
                "user": TaskSerializer(task, context=self.get_serializer_context()).data,
                "message": "Task Created Successfully.  Now perform Login to get your token",
            })
        else:
            raise Exception("Invalid Token")
        
    def get(self, request):
        page_num = int(request.GET.get("page", 1))
        limit_num = int(request.GET.get("limit", 10))
        start_num = (page_num - 1) * limit_num
        end_num = limit_num * page_num
        search_param = request.GET.get("search")
        task =TaskModel.filter().all()
        total_task = task.count()
        if search_param:
            task = task.filter(title__icontains=search_param)
        serializer = self.serializer_class(task[start_num:end_num], many=True)
        return Response({
            "status": "success",
            "total": total_task,
            "page": page_num,
            "last_page": math.ceil(total_task / limit_num),
            "task": serializer.data
        })


class TaskDetail(generics.GenericAPIView):
    # permission_classes = [AllButTaskCreatorGetReadOnly]
    queryset = TaskModel.objects.all()
    serializer_class = TaskSerializer

    def get_task(self, pk):
        try:
            return TaskModel.objects.get(pk=pk)
        except:
            return None

    def get(self, request, pk):
        # token = request.headers.get("authorization")
        # request.user.is_authenticated = authenticate(token=token)
        if not pk:
            return Response({"status": "Fail", "task": "Provide ID"})
        if request.user.is_authenticated:
            task = self.get_task(pk=pk)
            
            if task == None:
                return Response({"status": "fail", "message": f"task with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
            assigned_users = UserPermissionModel.objects.filter(task_id=pk).values('assigned_to_id')
            serializer = self.serializer_class(task)
            return Response({"status": "success", "task": serializer.data, "assigned_user":assigned_users})
        else:
            raise Exception("Invalid Token")

    def patch(self, request, pk):
        # token = request.headers.get("authorization")
        # request.user.is_authenticated = authenticate(token=token)
        
        if request.user.is_authenticated:
            task = self.get_task(pk)
            # self.check_object_permissions(obj=task, request=request)
            print(request.user.has_perm('task.change_task_model', task))
            print(request.user)
            if task == None:
                return Response({"status": "fail", "message": f"task with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
            if not request.user.has_perm('task.change_task_model', task):
                return Response({"status": "fail", "message": f"Request denied for user {request.user.username}"}, status=status.HTTP_403_FORBIDDEN)

            serializer = self.serializer_class(
                task, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.validated_data['updated_at'] = datetime.now()
                serializer.save()
                return Response({"status": "success", "task": serializer.data})
            return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Exception("Invalid Token")
             
            
# Register API
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
    queryset = User.objects.all()
    def delete(self, request, pk):
        if request.user.is_superuser:
            user = User.objects.get(pk=pk)
            if user == None:
                return Response({"status": "fail", "message": f"User with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)
            try:
                with transaction.atomic():
                    user.delete()
                    tasks = TaskModel.objects.filter(created_by_id=pk).all()
                    tasks.delete()
            except Exception:
                return Response({"status": "fail", "message": f"User with Id: {pk} not failed"}, status=status.HTTP_404_NOT_FOUND)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(message="Unauthorized. Super User req",status=status.HTTP_401_UNAUTHORIZED)


#BookMark APIs
class RegisterBookmark(generics.GenericAPIView):
    serializer_class = BookmarkSerializer
    queryset = BookmarkModel.objects.all()

    def post(self, request, *args,  **kwargs):
        
        if request.user.is_authenticated:
            data = request.data
            data["created_by"] = request.user.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                serializer.save()
                return Response({"status": "success", "bookmark": serializer.data}, status=status.HTTP_201_CREATED)
            else:
                return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        else:
            raise Exception("Invalid Token")

class BookmarkDetail(generics.GenericAPIView):
    serializer_class = BookmarkSerializer
    queryset = BookmarkModel.objects.all()

    def get_bookmark(self, pk):
        try:
            return BookmarkModel.objects.get(pk=pk)
        except:
            return None

    def delete(self, request, id):
        
        if request.user.is_authenticated:
            bookmark = self.get_bookmark(id)
            if bookmark == None:
                return Response({"status": "fail", "message": f"bookmark with Id: {id} not found"}, status=status.HTTP_404_NOT_FOUND)

            bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


#Comment API

class RegisterComment(generics.GenericAPIView):
    serializer_class = CommentSerializer
    queryset = CommentModel.objects.all()

    def post(self, request, *args,  **kwargs):
        
        if request.user.is_authenticated:
            
            # data_to_add = {
            #     'created_by_id': request.user.is_authenticated['id'],
            #     'task_id': request.data.task_id,
            #     'description': request.data.description,
            #     'created_by_name': request.data.created_by_name
            # }  
            data = request.data
            data['created_by'] = request.user.id
            serializer = self.serializer_class(data=data)
            try:
                with transaction.atomic():
                    if serializer.is_valid():
                        serializer.save()
                        print(request.data)
                        task = TaskModel.objects.select_for_update().filter(pk=request.data['task_id']).first()
                        task.total_comments +=1
                        task.save()
            except Exception as e:
                print(e)
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
        comment = CommentModel.objects.filter(task_id=request.data["task_id"]).all()
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

    def patch(self, request, pk):
        if request.user.is_authenticated:
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
        else:
            return Response({"status": "fail", "message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)

    def delete(self, request, pk):
        if request.user.is_authenticated:
            comment = self.get_comment(pk)
            if comment == None:
                return Response({"status": "fail", "message": f"comment with Id: {pk} not found"}, status=status.HTTP_404_NOT_FOUND)

            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response({"status": "fail", "message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED)


#Permission APIs

class RegisterPermission(generics.GenericAPIView):
    serializer_class = UserPermissionSerializer
    queryset = UserPermissionModel.objects.all()

    def post(self, request, *args,  **kwargs):
        # token = request.headers.get("authorization")
        # request.user.is_authenticated = authenticate(token=token)
        if request.user.is_authenticated:
            # if 'user' in request.data:
                
            #     data_to_add = {
            #         'created_by_id': request.user['id'],
            #         'assigned_to_id': request.data.assigned_to_id,
            #         'task_id': request.data.task_id,
            #         'assigned_person': request.data.user['name'],
            #         'permission': request.data.user['permission']
            #     }  
            serializer = self.serializer_class(data=request.data)
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
        
        if request.user.is_authenticated:
            Permission = self.get_permission(id)
            if Permission == None:
                return Response({"status": "fail", "message": f"Permission with Id: {id} not found"}, status=status.HTTP_404_NOT_FOUND)

            Permission.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def patch(self, request, pk):
        if request.user.is_authenticated:
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
        else:
            return Response({"status": "fail", "message": "Unauthorized"}, status=status.HTTP_401_UNAUTHORIZED) 

#UPvote comment API
class RegisterVote(generics.GenericAPIView):
    serializer_class = VoteSerializer
    queryset = VoteModel.objects.all()

    def post(self, request, *args,  **kwargs):
        
        user_vote = VoteModel.objects.filter(comment_id=request.data['comment_id'], created_by_id=request.user.id).first()
        if user_vote:
            return Response({"status": "fail", "message": "Already Voted"}, status=status.HTTP_403_FORBIDDEN)
        if request.user.is_authenticated:
            # data_to_add = {
            #     'created_by_id': request.user.is_authenticated['id'],
            #     'task_id': request.data.task_id,
            #     'comment_id': request.data.comment_id
            # }  
            serializer = self.serializer_class(data=request.data)
            try:
                with transaction.atomic():
                    if serializer.is_valid():
                        serializer.save()
                        comment = CommentModel.objects.select_for_update().filter(pk=request.data['comment_id']).first()
                        comment.up_votes +=1
                        comment.save()
            except Exception:
                return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "success", "comment": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            raise Exception("Invalid Token")
