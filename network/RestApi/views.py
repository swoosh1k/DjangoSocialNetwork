from rest_framework.response import Response
from rest_framework.views import APIView


from social.models import Post, User
from .serializers import getSerializer, UserSerializer, PostUpdateSerializer


class getView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = getSerializer(posts, many=True)
        return Response(serializer.data)

class UserView(APIView):
    def get(self, request):
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

class PostUpdateView(APIView):
    def put(self, request, pk):
        try:
            post = Post.objects.get(pk=pk)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PostUpdateSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)