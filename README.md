# ChatGPT-Django
ChatGPT를 사용한 Django 프로젝트
AI 기반 블로그 포스트 작성 도우미

# 서버 설치
https://nerogarret.tistory.com/47?category=800142

```
sudo apt-get update
sudo apt-get install python3-venv
sudo apt-get install libpq-dev
cd /srv
git clone [레포지토리 주소]
cd [프로젝트 이름]

python3 -m venv venv
source venv/bin/activate
pip3 install -r requirements.txt

pip install uwsgi

python3 manage.py runserver 0:8000
```
- 서버 실행 
sudo /srv/ChatGPT-Django-BE/venv/bin/uwsgi -i /srv/ChatGPT-Django-BE/.config/uwsgi/app.ini
# 요구사항

**모든 구현은 DRF를 이용하여서 구현**

1. 기본 프로젝트 설정 및 모델 설계:
- Django 프로젝트 생성 및 기본 설정
- User 모델 설계
- Chat 모델 설계

2. 회원가입과 로그인 구현:
- 회원가입 기능 구현
- 로그인 기능 구현

3. ChatGPT API 구현:
- ChatGPT로 요청을 보내주는 API 구현

4. 채팅 저장 기능 구현:
- 채팅 저장용 API 구현 APIView
- 사용자별 하루 5번 요청 제한 로직 추가

5. 채팅 조회 기능 구현:
- 저장된 채팅 내역 조회용 API 구현

6. 프론트엔드 연동:
- 프론트엔드에서 Django 서버를 통해 챗봇 API 요청 보내는 로직 구현
- API 응답값을 프론트엔드에 반영하는 로직 추가

# 개발하면서 만난 에러들

- 에러메세지
```
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency user.0001_initial on database 'default'.
```

- app.settings.py
```
INSTALLED_APPS = [
    'django.contrib.admin', # 주석처리
]
```

- app.urls.py
```
from django.contrib import admin #주석처리

urlpatterns = [
    path('admin/', admin.site.urls), #주석처리
]
```