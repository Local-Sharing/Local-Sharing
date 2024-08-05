from django.db import models
from accounts.models import User  

class Map(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()


class MapLikeUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    map = models.ForeignKey(Map, on_delete=models.CASCADE)

    class Meta:
        # constraints : 모델에 리스트 형태로 DB 제약 조건 설정 가능
        # UniqueConstraint : user, map 조합이 DB에 유일하게 저장되도록 설정
        # 동일한 유저가 동일한 맵에 대해 중복된 좋아요 선택 불가능
        constraints = [
            models.UniqueConstraint(fields=['user', 'map'], name='user-map-like')
        ]