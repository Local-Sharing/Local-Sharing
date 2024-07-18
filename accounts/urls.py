from django.urls import path
from . import views
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('signup/', views.SignupAPIView.as_views(), name='signup'),
    path('login/', TokenObtainPairView.as_view(), name='login'),
    path('token/', TokenRefreshView.as_view(), name='token_refresh'),
]
