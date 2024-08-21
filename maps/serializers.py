from rest_framework import serializers
from .models import Map, MapLikeUser


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'
        read_only_fields = ['created_at']


class MapSearchSerializer(serializers.Serializer):
    region = serializers.CharField(max_length = 100)
    weather = serializers.CharField(max_length=50)
    category = serializers.CharField(max_length=50, required=False)
    longitude = serializers.FloatField()
    latitude = serializers.FloatField()


class MapLikeUserSerializer(serializers.ModelSerializer):
    user_id = serializers.PrimaryKeyRelatedField(queryset=MapLikeUser.objects.all())
    map_id = serializers.PrimaryKeyRelatedField(queryset=Map.objects.all())
    
    class Meta:
        model = MapLikeUser
        fields = '__all__'

    def create(self, validated_data):
        user = self.context['request'].user
        title = self.context['request'].data.get('title')
        url = self.context['request'].data.get('url')
        region = self.context['request'].date.get('region')
        weather = self.context['request'].data.get('weather')
        category = self.context['request'].data.get('category')

        # 좋아요 누른 게시글 정보 map에 가져오거나 저장
        map_instance, created = Map.objects.get_or_create(
            title = title,
            url = url,
            region = region,
            weather = weather,
            category = category
        )

        # 좋아요 상태 확인, 처리
        like, created = MapLikeUser.objects.get_or_create(
            user = user,
            map = map_instance
        )

        if not created:
            like.delete()
            return None # 좋아요 취소
        return like # 좋아요 추가