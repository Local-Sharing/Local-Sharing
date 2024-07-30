from rest_framework import serializers
from .models import Post, Comment
from django.contrib.auth import get_user_model


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ['post_id', 'user_id', 'user_nickname']

    def create(self, validated_data):
        request = self.context.get('request')
        post = self.context.get('post')
        user = request.user

        comment = Comment(
            post_id=post,  
            user_id=user,  
            user_nickname=user.nickname,
            **validated_data
        )
        comment.save()
        return comment


User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(choices=Post.Category.choices)
    user_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    user_nickname = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = '__all__'
        read_only_fields = ['user_id', 'user_nickname', 'like', 'created_at', 'updated_at']

    def get_user_nickname(self, obj):
        return obj.user_id.nickname
