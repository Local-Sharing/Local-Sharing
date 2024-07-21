from django.shortcuts import get_object_or_404
from accounts.models import User
from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from accounts.serializers import UserSerializer
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.tokens import RefreshToken


class SignupAPIView(APIView):
    # 회원가입
    def post(self, request):
        serializer = UserSerializer(data=request.data)
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
        

class ProfileAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # 프로필 조회
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=200)
    

class ProfileUpdateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # 프로필 수정
    def put(self, request, pk):
        user = get_object_or_404(get_user_model(), pk=pk)


class UserDeleteAPIView(APIView):
    permission_classes = [IsAuthenticated]

    # 회원탈퇴
    def delete(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        password = request.data.get('password')
        if password is None:
            return Response({'error' : '비밀번호를 입력해주세요.'}, status=400)
        
        if user.check_password(password):
            user.delete()
            return Response({'message' : '회원 탈퇴가 완료되었습니다.'}, status=200)
        return Response({'error' : '비밀번호가 일치하지 않습니다.'}, status=400)