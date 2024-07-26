from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post']


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Post.Category.choices)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user_id', 'user_nickname', 'like', 'created_at', 'updated_at']

