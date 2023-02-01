from rest_framework import generics, status
from rest_framework.response import Response
from jwtauthloginandregister.bookmark.serializer import BookmarkSerializer
from jwtauthloginandregister.settings import SECRET_KEY
from django.contrib.auth.models import User

from models import BookmarkModel
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

class RegisterBookmark(generics.GenericAPIView):
    serializer_class = BookmarkSerializer
    queryset = BookmarkModel.objects.all()

    def post(self, request, *args,  **kwargs):
        token = request.headers.get("authorization")
        authenticated = authenticate(token=token)
        if authenticated:
            serializer = self.serializer_class(data=request.data)
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
        token = request.headers.get("authorization")
        authenticated = authenticate(token=token)
        if authenticated:
            bookmark = self.get_bookmark(id)
            if bookmark == None:
                return Response({"status": "fail", "message": f"bookmark with Id: {id} not found"}, status=status.HTTP_404_NOT_FOUND)

            bookmark.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
