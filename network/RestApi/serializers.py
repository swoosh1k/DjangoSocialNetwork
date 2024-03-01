from rest_framework import serializers
from social.models import Post

# from .models import api

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'



