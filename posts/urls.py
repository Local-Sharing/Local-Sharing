from django.urls import path
from . import views


urlpatterns = [
    path('', views.PostListAPIView.as_view(), name='post-list'),
    path('<int:post_id>/',views.PostDetailAPIView.as_view(), name='post-detail'),
    path('<int:post_id>/like/', views.PostLikeAPIView.as_view(), name='post-like'),
    path('user/<int:user_id>/', views.UserPostView.as_view(), name='user-post'),
    path('user/<int:user_id>/like/', views.UserLikePostAPIView.as_view(), name='user-like-post'),
]