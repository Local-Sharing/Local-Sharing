from django.shortcuts import render
from django.contrib.auth import logout
from rest_framework.views import APIView
from accounts.serializers import SignupSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken


class SignupAPIView(APIView):
    # 회원가입
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)
    

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # 로그아웃
    def post(self, request):
        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=200)
        except Exception as e:
            print(f"Exception: {e}") 
            return Response(status=400)