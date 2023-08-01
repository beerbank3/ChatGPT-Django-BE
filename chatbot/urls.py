from django.urls import path
from .views import ChatView,ChatRemove

app_name = 'chatbot'

urlpatterns = [
	path('', ChatView.as_view(), name='index'),
    # 삭제
	path('delete/', ChatRemove.as_view(), name='delete'),
]