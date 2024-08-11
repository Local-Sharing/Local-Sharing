import requests
from django.shortcuts import render, get_object_or_404
from LocalSharing.config import KAKAO_REST_API_KEY
from rest_framework.views import APIView
from maps.models import Map, MapLikeUser
from maps.serializers import MapSerializer, MapLikeUserSerializer


def kakao_rest_api(longitude, latitude):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json'
    headers = {'Authorization': f'KakaoAK {KAKAO_REST_API_KEY}'}
    params = {'x': longitude, 'y': latitude}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


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

