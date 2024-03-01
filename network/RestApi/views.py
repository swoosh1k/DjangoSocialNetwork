from rest_framework.response import Response
from rest_framework.views import APIView


from social.models import Post
from .serializers import PostSerializer


class PostView(APIView):
    def get(self, request):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)