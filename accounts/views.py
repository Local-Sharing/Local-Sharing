from django.shortcuts import render
from rest_framework.views import APIView
from accounts.serializers import SignupSerializer
from rest_framework.response import Response


class SignupAPIView(APIView):
    # 회원가입
    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            if user:
                return Response(serializer.data, status=200)
        return Response(serializer.errors, status=400)