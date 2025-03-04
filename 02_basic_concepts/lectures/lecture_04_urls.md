# Лекция 4: URLs

## Введение
URL-маршрутизация в Django определяет, как запросы пользователя направляются к соответствующим views. Это важная часть архитектуры вашего приложения.

---

## Основные концепции

### 1. Настройка URL-маршрутов

URL-маршруты определяются в файле `urls.py`. Пример:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
    path('articles/<int:id>/', views.article_detail, name='article_detail'),
]
```

- `path('', views.home, name='home')`: Главная страница.
- `path('articles/', views.article_list, name='article_list')`: Список статей.
- `path('articles/<int:id>/', views.article_detail, name='article_detail')`: Детальная страница статьи.

---

### 2. Передача параметров

Вы можете передавать параметры через URL. Например:

```python
def article_detail(request, id):
    article = Article.objects.get(id=id)
    return render(request, 'article_detail.html', {'article': article})
```

URL для этого view будет выглядеть так: `/articles/1/`.

---

### 3. Именованные маршруты

Именованные маршруты позволяют ссылаться на них в коде. Например:

```python
<a href="{% url 'article_detail' id=article.id %}">{{ article.title }}</a>
```

---

### 4. Включение URL-маршрутов приложения

Вы можете разделить URL-маршруты между приложениями. Например:

#### В `myapp/urls.py`:
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('articles/', views.article_list, name='article_list'),
]
```

#### В основном `urls.py`:
```python
from django.urls import include, path

urlpatterns = [
    path('myapp/', include('myapp.urls')),
]
```

---

## Заключение

В этой лекции мы рассмотрели основы работы с URL-маршрутизацией в Django. Вы научились:
- Настроить URL-маршруты.
- Передавать параметры через URL.
- Использовать именованные маршруты.
- Разделять URL-маршруты между приложениями.

Переходите к практическим заданиям: [Tasks](../practice/tasks.md)