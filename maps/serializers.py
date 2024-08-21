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
    longitude = serializers.FloatField(required=False)
    latitude = serializers.FloatField(required=False)


class MapLikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLikeUser
        fields = '__all__'
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        map_instance = validated_data.get('map')

        # 좋아요를 추가하는 경우에만 create 호출
        return MapLikeUser.objects.create(user=user, map=map_instance)

