from django.shortcuts import redirect
from django.views import View
from django.contrib.auth import authenticate, logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authtoken.models import Token
from datetime import date
from .serializers import UserSerializer, LoginSerializer
from .models import User

### Registration
class Registration(APIView):

    def post(self, request):
        try:
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                user = serializer.instance  # 새로 생성된 사용자 객체 가져오기
                token, _ = Token.objects.get_or_create(user=user)
                today = date.today()
                return Response({'message': f'{user.name}님 반갑습니다.', 'token': token.key, 'date':today}, status=status.HTTP_201_CREATED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

### Login
class Login(APIView):

    def post(self, request):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid():
                email = serializer.validated_data['email']
                password = serializer.validated_data['password']

                user = authenticate(email=email, password=password)
                if user:
                    token, _ = Token.objects.get_or_create(user=user)
                    today = date.today()
                    return Response({'token': token.key, 'date':today}, status=status.HTTP_200_OK)
                else:
                    return Response({'error': '유효하지 않은 인증 정보입니다.'}, status=status.HTTP_401_UNAUTHORIZED)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


### Logout
class Logout(APIView):
    def post(self, request):
        try:
            # 사용자의 토큰 가져오기
            auth_token = request.META.get('HTTP_AUTHORIZATION')
            if auth_token:
                # "Token <토큰값>" 형식에서 "토큰값"만 추출
                token = auth_token.split()[1]

                # 토큰 삭제하여 로그아웃 처리
                Token.objects.filter(key=token).delete()

            return Response({'message': '로그아웃되었습니다.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
