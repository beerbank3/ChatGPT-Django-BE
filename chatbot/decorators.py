from functools import wraps
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.response import Response
from rest_framework import status


def token_required(view_func):
    @wraps(view_func)
    def _wrapped_view(request, *args, **kwargs):
        auth = TokenAuthentication()
        try:
            user, token = auth.authenticate(request)
        except AuthenticationFailed:
            return Response({'error': '유효하지 않은 인증 정보입니다.'}, status=status.HTTP_401_UNAUTHORIZED)

        # 받아온 토큰과 유저 정보를 뷰 함수에 전달
        return view_func(request, user, token, *args, **kwargs)

    return _wrapped_view