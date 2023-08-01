# chatbot/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from dotenv import load_dotenv
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
from django.db.models import Count, Min
from datetime import datetime, date
import openai
import os
from django.db import models
from .models import Conversation
from .decorators import token_required

load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')

class ChatView(APIView):
    @method_decorator(token_required)
    def dispatch(self, request, user, token, *args, **kwargs):
        self.user = user  # 유저 정보를 클래스의 속성으로 저장
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        today = date.today()
        if request.GET.get('date') and request.GET.get('date') != "undefined":
            today = request.GET.get('date')
        # 오늘 날짜의 대화 기록을 가져옵니다.
        conversations_today = Conversation.objects.filter(user=self.user, created_at__date=today)
        serialized_conversations_today = [
            {
                'question': conversation.question,
                'answer': conversation.answer,
                'created_at': conversation.created_at,
            }
            for conversation in conversations_today
        ]

        conversations_other_dates = Conversation.objects.filter(user=self.user).values('created_at__date').annotate(count=Count('created_at__date'), first_question=Min('question')).order_by('-created_at__date')
        serialized_conversations_other_dates = [
            {
                'date': item['created_at__date'],
                'count': item['count'],
                'first_question': item['first_question'],
            }
            for item in conversations_other_dates
        ]

        # 결과를 합쳐서 Response로 반환합니다.
        serialized_conversations = {
            'conversations_today': serialized_conversations_today,
            'conversations_other_dates': serialized_conversations_other_dates,
        }
        return Response(serialized_conversations)
    
    # @method_decorator(ratelimit(key='user', rate='5/d'))
    def post(self, request, *args, **kwargs):
        if 'messages' not in request.session:
            request.session['messages'] = [
                {"role": "system", "content": "너는 AI 블로그 도우미야"},
            ]
        
        prompt = request.POST.get('prompt')
        date = request.POST.get('date')
        if prompt:
            temperature = float(request.POST.get('temperature', 0.1))

            request.session['messages'].append({"role": "user", "content": prompt})
            request.session.modified = True

            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=request.session['messages'],
                temperature=temperature,
                max_tokens=1000,
            )

            formatted_response = response['choices'][0]['message']['content']
            if request.user.is_authenticated:
                user = request.user
            else:
                user = None
            conversation = Conversation(user=user, question=prompt, answer=formatted_response, created_at=date)
            conversation.save()

            request.session['messages'].append({"role": "assistant", "content": formatted_response})
            request.session.modified = True

            messages = {
                'messages' : request.session['messages']
            }
            return Response(messages)
    

class ChatRemove(APIView):

    @method_decorator(token_required)
    def dispatch(self, request, user, token, *args, **kwargs):
        self.user = user  # 유저 정보를 클래스의 속성으로 저장
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        date_str = request.POST.get('date')  # 요청으로 받은 날짜 데이터
        try:
            date = datetime.strptime(date_str, '%Y-%m-%d')
            conversations = Conversation.objects.filter(created_at__date=date,user=self.user).values('question', 'created_at').annotate(count=models.Count('id'))
            for conversation in conversations:
                if conversation['count'] > 1:
                    Conversation.objects.filter(question=conversation['question'], created_at=conversation['created_at']).update(is_delete=True)
            return Response({'message': 'is_delete를 수정하였습니다.'}, status=status.HTTP_200_OK)
        except ValueError:
            return Response({'message': '잘못된 날짜 형식입니다. YYYY-MM-DD 형식으로 입력해주세요.'}, status=status.HTTP_200_OK)
    