import requests
from openai import OpenAI
from django.shortcuts import render, get_object_or_404
from LocalSharing.config import KAKAO_REST_API_KEY, OPEN_AI_KEY
from datetime import datetime, timedelta
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from maps.models import Map, MapLikeUser, WeatherCategoryMapping
from maps.serializers import MapSerializer, MapSearchSerializer, MapLikeUserSerializer


# KAKAO API를 사용하여 위치 정보 반환
def kakao_rest_api(region, category):
    url = 'https://dapi.kakao.com/v2/local/search/keyword.json'
    headers = {'Authorization': f'KakaoAK {KAKAO_REST_API_KEY}'}
    query = f'{region} {category}' if category else region
    params = {
        'query': query,
        'size': 10
    }

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        return None


# OpenAI API를 사용하여 게시글 검색
# def openai_api_search(region, weather, category):
#     client = OpenAI(api_key=OPEN_AI_KEY)
#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system", "content": "You are a helpful assistant."},
#             {"role": "user", 
#             "content": f"Can you suggest some blog posts or resources in the {category} category located in {region} with {weather} weather conditions?"
#             }
#         ]
#     )
#     return completion.choices[0].message.content


# 지역, 날씨 조건을 기반으로 최근 1년 내의 게시글 필터링
def map_search(region, weather, category=None):
    # datetime : 현재시간 / timedelta : datetime 객체의 더하기, 빼기 수행 가능
    one_year_ago = datetime.now() - timedelta(days=365)

    # 지역과 날씨 조건으로 게시글 검색
    # values_list : 값을 튜플 형태로 리스트에 담아 반환 // 예 : [('관광명소',), ('음식점',), ('쇼핑',)]
    # flat=True : 반환되는 리스트를 평평하게 만들어줌 -> 튜플이 아닌 일반 값으로 리스트를 구성하게 한다. 한개의 필드만 요청했을 때만 사용 가능 // 예 : ['관광명소', '음식점', '쇼핑']
    if category is None:
        categories = WeatherCategoryMapping.objects.filter(weather=weather).values_list('category', flat=True)
    else:
        categories = [category]

    # category__in=categories : category 필드가 categories 리스트 내 하나의 값을 갖는 Mao 객체를 찾음
    search_result = Map.objects.filter(region=region, weather=weather, category__in=categories)
    return search_result.filter(created_at__gte=one_year_ago)

class MapListAPIView(APIView):
    # 검색
    def post(self, request):
        serializer = MapSearchSerializer(data = request.data)
        if serializer.is_valid():
            region = serializer.validated_data['region']
            weather = serializer.validated_data['weather']
            category = serializer.validated_data.get('category')

            # KAKAO API로 위치 검색
            places = kakao_rest_api(region, category)
            if not places:
                return Response({'error' : '위치 데이터를 찾지 못했습니다.'}, status=400)        

            # 위치 리스트 반환
            if len(places['documents']) > 1:
                return Response({'places': places['documents']}, status=200)
            
            if len(places['documents']) == 0:
                return Response({'error': '해당 조건에 맞는 장소를 찾지 못했습니다.'}, status=404)
            
            # 한개의 장소만 찾았다면 해당 장소를 Map 모델에 저장
            place = places['documents'][0]
            map_instance, created = Map.objects.get_or_create(
                title=place['place_name'],
                region=place['address_name'],
                weather=weather,
                category=category,
                longitude=place['x'],
                latitude=place['y'],
                defaults={'url': place.get('place_url', '')}
            )

            # 지도 검색 및 필터링
            search_result = map_search(region, weather, category)
            if not search_result.exists():
                return Response({'message':'게시글이 없습니다.'}, status=400)
            
            map_serializer = MapSerializer(search_result, many=True)
            return Response({
                'location': place,
                'map_id': map_instance.id,
                'posts': map_serializer.data
            }, status=200)
        return Response(serializer.errors, status=400)


class MapSaveAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        place_data = request.data.get('place')
        if not place_data:
            return Response({'error': '장소 정보가 필요합니다.'}, status=400)
        
        map_instance, created = Map.objects.get_or_create(
            title=place_data['place_name'],
            region=place_data['address_name'],
            longitude=place_data['x'],
            latitude=place_data['y'],
            defaults={'url': place_data.get('place_url', '')}
        )
        
        if created:
            return Response({'message': '장소가 저장되었습니다.', 'map_id': map_instance.id}, status=201)
        else:
            return Response({'message': '이미 존재하는 장소입니다.', 'map_id': map_instance.id}, status=200)


class MapLikeAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request, map_id):
        map_instance = get_object_or_404(Map, id=map_id)
        user = request.user

        # 좋아요가 이미 존재하는지 확인
        try:
            like = MapLikeUser.objects.get(user=user, map=map_instance)
            like.delete()
            return Response({'message': '좋아요 취소'}, status=200)
        except MapLikeUser.DoesNotExist:
            # 좋아요가 없는 경우 추가
            data = {'map': map_instance.id}
            serializer = MapLikeUserSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response({'message': '좋아요'}, status=200)
            return Response(serializer.errors, status=400)


class UserProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        liked_maps = MapLikeUser.objects.filter(user=user)

        map_ids = liked_maps.values_list('map', flat=True)
        liked_maps_data = Map.objects.filter(id__in=map_ids)

        serializer = MapSerializer(liked_maps_data, many=True)
        return Response(serializer.data, status=200)