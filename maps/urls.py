from django.urls import path
from . import views


urlpatterns = [
    path('', views.MapListAPIView.as_view(), name='map-list'),
    path('<int:map_id>/like/', views.MapLikeAPIView.as_view(), name='map-like'),
    path('save/', views.MapSaveAPIView.as_view(), name='map-create'),
]
