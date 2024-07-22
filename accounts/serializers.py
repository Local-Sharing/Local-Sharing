from rest_framework import serializers
from .models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

    def create(self, validated_data):
        user = User.objects.create_user(
            username = validated_data['username'],
            first_name = validated_data['first_name'],
            last_name = validated_data['last_name'],
            email = validated_data['email'],
            password = validated_data['password'],
            nickname = validated_data['nickname'],
            gender = validated_data['gender'],
            age = validated_data['age'],
            image = validated_data.get('image')# image 추가
        )
        return user
    

class ProfileUpdateSerialize(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['nickname', 'email', 'image']

    def validate_email(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "사용중인 이메일 입니다."})
        return value
    
    def validate_nickname(self, value):
        user = self.instance
        if User.objects.exclude(pk=user.pk).filter(nickname=value).exists():
            raise serializers.ValidationError({"nickname": "사용중인 닉네임 입니다."})
        return value
    
    def update(self, instance, validated_data):
        instance.email = validated_data.get('email', instance.email)
        instance.nickname = validated_data.get('nickname', instance.nickname)
        instance.image = validated_data.get('image', instance.image)
        instance.save()
        return instance


class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['password']

    def validate_password(self, value):
        if len(value) < 8:
            raise serializers.ValidationError('비밀번호는 8글자 이상이어야 합니다.')
        return value
    
    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance