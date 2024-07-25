from django.shortcuts import render
from rest_framework.views import APIView
from posts.models import Post, Comment
from posts.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
import uuid


class PostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 게시판 조회
    def get(self, request):


        post = Post.objects.all()
        serializer = PostSerializer(post, many=True)
        return Response(serializer.data)

    # 게시글 생성
    def post(self, request):
        # 이미지 이름을 유효 아이디로 해싱
        request.data.image = f'accounts_{uuid.uuid4()}.png'
        serializer = PostSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)