from django.shortcuts import render, get_object_or_404
from rest_framework.views import APIView
from posts.models import Post, Comment
from accounts.models import User
from posts.serializers import PostSerializer, CommentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from rest_framework.response import Response
from urllib.parse import unquote
from django.db.models import Q, Count


class PostListAPIView(APIView):
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
    

class PostDetailAPIView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    # post_id를 기준으로 Post 객체를 DB에서 가져옴
    def get_object(self, post_id):
        return get_object_or_404(Post, pk=post_id)

    # 게시글 상세 조회
    def get(self, request, post_id):
        post = self.get_object(post_id)
        serializer = PostSerializer(post)
        data = serializer.data

        # 사용자가 좋아요 눌렀는지 여부 확인
        like = False
        if request.user.is_authenticated:
            if request.user.id in post.like.values_list('id', flat=True): 
                like = True

        # 댓글 조회
        comments = Comment.objects.filter(post_id=post_id)
        comment_serializer = CommentSerializer(comments, many=True)
        data['comments'] = comment_serializer.data

        data = {'data':data, 'like':like}
        return Response(data, status=200)
        
    # 게시글 수정
    def put(self, request, post_id):
        post = self.get_object(post_id)
        if post.user_id != request.user:
            return Response({'detail': '권한이 없습니다.'}, status=403)
        serializer = PostSerializer(post, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)

    # 게시글 삭제
    def delete(self, request, post_id):
        post = self.get_object(post_id)
        if post.user_id != request.user:
            return Response({'detail': '권한이 없습니다.'}, status=403)
        post.delete()
        return Response(status=200)
    
    # 댓글 작성
    def post(self, request, post_id):
        post = self.get_object(post_id)
        serializer = CommentSerializer(data=request.data, context={'request': request, 'post': post})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=200)


class PostLikeAPIView(APIView):
    def get_object(self, post_id):
        return get_object_or_404(Post, pk=post_id)

    # 게시글 좋아요
    def post(self, request, post_id):
        post = self.get_object(post_id)
        if post.like.filter(pk=request.user.id).exists():
            post.like.remove(request.user.id)
        else:
            post.like.add(request.user.id)
        return Response(status=200)


class UserPostView(APIView):
    # 유저가 작성한 게시글 목록
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        post = Post.objects.filter(user_id=user)
        serilaizer = PostSerializer(post, many=True)
        return Response(serilaizer.data, status=200)


class UserLikePostAPIView(APIView):
    # 사용자가 좋아요 누른 게시글 조회
    def get(self, request, user_id):
        user = get_object_or_404(User, pk=user_id)
        like_post = user.post_like.all()
        serializer = PostSerializer(like_post, many=True)
        return Response(serializer.data, status=200)