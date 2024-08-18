import requests
from openai import OpenAI
from django.shortcuts import render, get_object_or_404
from LocalSharing.config import KAKAO_REST_API_KEY, OPEN_AI_KEY
from datetime import datetime, timedelta
from rest_framework.views import APIView
from rest_framework.response import Response
from maps.models import Map, MapLikeUser
from maps.serializers import MapSerializer, MapSearchSerializer, MapLikeUserSerializer


# KAKAO API를 사용하여 위치 정보 반환
def kakao_rest_api(longitude, latitude):
    url = 'https://dapi.kakao.com/v2/local/geo/coord2regioncode.json'
    headers = {'Authorization': f'KakaoAK {KAKAO_REST_API_KEY}'}
    params = {'x': longitude, 'y': latitude}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# OpenAI API를 사용하여 게시글 검색
def openai_api_search(region, weather, category):
    client = OpenAI(api_key=OPEN_AI_KEY)
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", 
            "content": "Search for posts in the category {category} within the region {region} and with weather condition {weather}."
            }
        ]
    )
    return completion.choices[0].message.get('content', '')


# 지역, 날씨 조건을 기반으로 최근 1년 내의 게시글 필터링
def map_search(region, weather, category=None):
    # datetime : 현재시간 / timedelta : datetime 객체의 더하기, 빼기 수행 가능
    one_year_ago = datetime.now() - timedelta(days=365)

    # 지역과 날씨 조건으로 게시글 검색
    search_results = Map.objects.filter(region=region, weather=weather)
    if category:
        search_results = search_results.filter(category=category)

    return search_results.filter(created_at__gte = one_year_ago)

class MapListAPIView(APIView):
    # 검색
    def post(self, request):
        serializer = MapSearchSerializer(data = request.data)
        if serializer.is_valid():
            region = serializer.validated_data['region']
            weather = serializer.validated_data['weather']
            category = serializer.validated_data.get('category')
            longitude = serializer.validated_data['longitude']
            latitude = serializer.validated_data['latitude']

            # KAKAO API로 위치 검색
            location_data = kakao_rest_api(longitude, latitude)
            if not location_data:
                return Response({'error' : '위치 데이터를 찾지 못했습니다.'}, status=400)
            
            # OpenAI API로 카테고리 게시글 검색
            openai_data = openai_api_search(region, weather, category)

            # 지도 검색 및 필터링
            search_result = map_search(region, weather, category)
            if not search_result.exists():
                return Response({'message':'게시글이 없습니다.'}, status=400)
            
            map_serializer = MapSerializer(search_result, many=True)
            return Response({
                'location_data' : location_data,
                'openai_data' : openai_data,
                'posts' : map_serializer.data
            }, status=200)
        return Response(serializer.errors, status=400)


class MapLikeAPIView(APIView):
    # 특정 지역 좋아요 목록
    def post(self, request, map_id):
        serializer = MapLikeUserSerializer(data=request.data, context={'request':request})
        if serializer.is_valid():
            like = serializer.save()
            if like:
                return Response({'message' : '좋아요'}, status=200)
            else:
                return Response({'message' : '좋아요 삭제'}, status=200)
        return Response(serializer.errors, status=400)


class UserProfileAPIView(APIView):
    def get(self, request):
        user = request.user
        liked_maps = MapLikeUser.objects.filter(user=user)

        map_ids = liked_maps.values_list('map', flat=True)
        liked_maps_data = Map.objects.filter(id__in=map_ids)

        serializer = MapSerializer(liked_maps_data, many=True)
        return Response(serializer.data, status=200)

