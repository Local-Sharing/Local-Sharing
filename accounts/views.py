from django.shortcuts import render
from rest_framework import APIView


class SignupAPIView(APIView):
    # 회원가입
    def post(self, request):
        pass