from rest_framework import serializers
from social.models import Post, User

# from .models import api

class getSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'

class PostUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ['creater', 'context_text', 'context_image']


    def update(self, instance, validated_data):
        # Обновление данных в модели на основе валидированных данных
        instance.creater = validated_data.get('creater', instance.creater)
        instance.context_text = validated_data.get('context_text', instance.context_text)
        instance.context_image = validated_data.get('context_image', instance.context_image)
        instance.save()
        return instance



