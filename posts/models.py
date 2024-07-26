from django.db import models
from django.conf import settings


class Post(models.Model):
    class Category(models.TextChoices):
        PLACE_SHARE = 'PS', '장소공유'
        FREE_BOARD = 'FB', '자유게시판'

    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    user_nickname = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=2, choices=Category.choices)
    image = models.ImageField(upload_to='media/posts/', null=True, blank=True)
    like = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='post_like')


class Comment(models.Model):
    user_id = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    post_id = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    content = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user_nickname = models.CharField(max_length=20)
    image = models.ImageField(upload_to='media/posts/', null=True, blank=True)