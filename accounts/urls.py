from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenBlacklistView,
)


urlpatterns = [
    path('signup/', views.SignupView.as_view(), name='signup-page'),
    path('api/signup/', views.SignupAPIView.as_view(), name='signup'),
    path('login/', views.LoginView.as_view(), name='login-page'),
    path('api/login/', TokenObtainPairView.as_view(), name='login'),
    path('store_tokens/', views.store_tokens, name='store_tokens'),
    path('token/', TokenRefreshView.as_view(), name='token_refresh'),
    path('logout/', views.LogoutAPIView.as_view(), name='logout'),
    path('profile/<int:pk>/', views.ProfileAPIView.as_view(), name='profile'),
    path('profile/<int:pk>/update/', views.ProfileUpdateAPIView.as_view(), name='profile-update'),
    path('profile/<int:pk>/change-password/', views.ChangePasswordAPIView.as_view(), name='change-password'),
    path('profile/<int:pk>/delete/', views.UserDeleteAPIView.as_view(), name='delete'),
]
