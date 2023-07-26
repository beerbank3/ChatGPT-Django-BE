from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from .models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=200)

    def validate(self, data):
        email = data.get('email', None)
        password = data.get('password', None)

        user = authenticate(email=email, password=password)

        if not user:
            raise serializers.ValidationError('유효하지 않은 인증 정보입니다.')

        data['user'] = user  # 유효한 사용자 객체를 검증 데이터에 추가

        return data

    def create(self, validated_data):
        user = validated_data['user']

        # 토큰 생성 또는 기존 토큰 가져오기
        token, _ = Token.objects.get_or_create(user=user)
        
        # 검증 데이터에 토큰 추가
        validated_data['token'] = token.key
        return validated_data