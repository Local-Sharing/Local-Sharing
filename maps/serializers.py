from rest_framework import serializers
from .models import Map, MapLikeUser


class MapSerializer(serializers.ModelSerializer):
    class Meta:
        model = Map
        fields = '__all__'


class MapLikeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MapLikeUser
        fields = '__all__'