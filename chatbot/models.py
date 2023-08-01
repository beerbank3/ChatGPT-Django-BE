from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class Conversation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    created_at = models.DateTimeField(auto_now_add=False, blank=True, null=True)
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.created_at
    
    def save(self, *args, **kwargs):
        # 만약 created_at 필드에 데이터가 없다면 현재 시간을 저장합니다.
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)