from rest_framework import serializers
from social.models import Post, User

# from .models import api

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'