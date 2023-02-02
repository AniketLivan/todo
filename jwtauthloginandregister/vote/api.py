from datetime import datetime
from django.db import transaction
from rest_framework import generics, status
from rest_framework.response import Response
from jwtauthloginandregister.settings import SECRET_KEY
from django.contrib.auth.models import User
from .models import VoteModel
from comment.models import CommentModel
from .serializer import VoteSerializer
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

class RegisterVote(generics.GenericAPIView):
    serializer_class = VoteSerializer
    queryset = VoteModel.objects.all()

    def post(self, request, *args,  **kwargs):
        token = request.headers.get("authorization")
        authenticated = authenticate(token=token)
        user_vote = VoteModel.objects.get(comment_id=request.data.comment_id)
        if user_vote:
            return Response({"status": "fail", "message": "Already Voted"}, status=status.HTTP_403_FORBIDDEN)
        if authenticated:
            data_to_add = {
                'created_by_id': authenticated['id'],
                'task_id': request.data.task_id,
                'comment_id': request.data.comment_id
            }  
            serializer = self.serializer_class(data=data_to_add)
            try:
                with transaction.atomic():
                    serializer.save()
                    comment = CommentModel.objects.filter(pk=request.data.comment_id).select_for_update().get() 
                    comment.validated_data['up_votes'] += 1
                    comment.save()
            except Exception:
                return Response({"status": "fail", "message": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
            return Response({"status": "success", "comment": serializer.data}, status=status.HTTP_201_CREATED)
        else:
            raise Exception("Invalid Token")
