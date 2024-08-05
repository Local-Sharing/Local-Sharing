from django.shortcuts import render, get_object_or_404
from . import config
from rest_framework.views import APIView
from maps.models import Map, MapLikeUser
from maps.serializers import MapSerializer, MapLikeUserSerializer


class MapListAPIView(APIView):
    # 지도 조회 및 검색 결과
    def get(self, request):
        pass

    # 지도 검색
    def post(self, request):
        pass


class MapLikeAPIView(APIView):
    # 특정 지역 좋아요 등록
    def post(self, request, map_id):
        # 좋아요 목록이 있으면 좋아요 취소 로직
        pass

