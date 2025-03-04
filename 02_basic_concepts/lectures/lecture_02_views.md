# Лекция 2: Views

## Введение
Views — это функции или классы, которые обрабатывают HTTP-запросы и возвращают HTTP-ответы. Они являются центральной частью логики вашего приложения.

Django поддерживает два типа views:
1. Функциональные views.
2. Классовые views.

---

## 1. Функциональные views

Простой пример функционального view:

```python
from django.http import HttpResponse

def home(request):
    return HttpResponse("Добро пожаловать на главную страницу!")
```

---

## 2. Классовые views

Классовые views предоставляют больше возможностей и лучше подходят для сложных задач. Например, `TemplateView` позволяет легко рендерить шаблоны:

```python
from django.views.generic import TemplateView

class HomePageView(TemplateView):
    template_name = "home.html"
```

---

## 3. Работа с запросами

Вы можете получить доступ к параметрам запроса через объект `request`:

```python
def greet_user(request, name):
    return HttpResponse(f"Hello, {name}!")
```

---

## 4. Рендеринг шаблонов

Часто вам нужно отобразить HTML-страницу. Для этого используется функция `render`:

```python
from django.shortcuts import render

def article_detail(request, id):
    article = Article.objects.get(id=id)
    return render(request, 'article_detail.html', {'article': article})
```

---

## Заключение

В этой лекции мы рассмотрели основы работы с views в Django. Вы научились:
- Создавать функциональные и классовые views.
- Работать с запросами.
- Рендерить шаблоны.

Переходите к следующей лекции: [Templates](../lecture_03_Templates.md)