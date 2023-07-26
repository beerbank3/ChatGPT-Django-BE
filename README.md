# ChatGPT-Django
ChatGPT를 사용한 Django 프로젝트

# 개발하면서 만난 에러들
```
django.db.migrations.exceptions.InconsistentMigrationHistory: Migration admin.0001_initial is applied before its dependency user.0001_initial on database 'default'.
```

app.settings.py
```
INSTALLED_APPS = [
    'django.contrib.admin', # 주석처리
]
```

app.urls.py
```
from django.contrib import admin #주석처리

urlpatterns = [
    path('admin/', admin.site.urls), #주석처리
]
```