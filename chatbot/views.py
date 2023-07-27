# chatbot/views.py
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from dotenv import load_dotenv
from django.utils.decorators import method_decorator
from django_ratelimit.decorators import ratelimit
import openai
import os
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
        conversations = Conversation.objects.filter(user=self.user)
        serialized_conversations = [
            {
                'question': conversation.question,
                'answer': conversation.answer,
                'created_at': conversation.created_at,
            }
            for conversation in conversations
        ]
        return Response({'conversations': serialized_conversations})
    
    @method_decorator(ratelimit(key='user', rate='5/d'))
    def post(self, request, *args, **kwargs):
        prompt = request.POST.get('prompt')
        if prompt:
            # 이전 대화 기록 가져오기
            session_conversations = request.session.get('conversations', [])
            previous_conversations = "\n".join([f"User: {c['prompt']}\nAI: {c['response']}" for c in session_conversations])
            prompt_with_previous = f"{previous_conversations}\nUser: {prompt}\nAI:"

            model_engine = "text-davinci-003"
            completions = openai.Completion.create(
                engine=model_engine,
                prompt=prompt_with_previous,
                max_tokens=1024,
                n=5,
                stop=None,
                temperature=0.5,
            )
            response = completions.choices[0].text.strip()

            if request.user.is_authenticated:
                user = request.user
            else:
                user = None
            conversation = Conversation(user=user, question=prompt, answer=response)
            conversation.save()

            # 대화 기록에 새로운 응답 추가
            session_conversations.append({'prompt': prompt, 'response': response})
            request.session['conversations'] = session_conversations
            request.session.modified = True

        return self.get(request, *args, **kwargs)