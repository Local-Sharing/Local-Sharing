from django.shortcuts import render
from rest_framework.views import APIView
from posts.models import Post, Comment
from posts.serializers import PostSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
import uuid
from urllib.parse import unquote
from django.db.models import Q, Count


class PostList(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # 게시판 조회
    def get(self, request):
        search_query = unquote(request.GET.get('search', ''))
        category = request.GET.get('category')
        sort = request.GET.get('sort', '-created_at')

        posts = Post.objects.all()

        if search_query:
            posts = posts.filter(
                Q(title__icontains=search_query) | Q(content__icontains=search_query) | Q(user_nickname__icontains=search_query)
            )

        if category:
            posts = posts.filter(category=category)

        posts = posts.annotate(likes_count=Count('like'))

        if sort == '-like':
            posts = posts.order_by('-likes_count', '-created_at')
        else:
            posts = posts.order_by(sort)

        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

    # 게시글 생성
    def post(self, request):
        data = request.data.copy()
        data['user_id'] = request.user.id

        if 'image' in request.FILES:
            data['image'] = request.FILES.get('image')

        serializer = PostSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)