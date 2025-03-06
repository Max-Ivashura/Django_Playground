# Лекция 4: Middleware

## Введение
Middleware — это слой, который обрабатывает запросы и ответы до/после views.

---

### Пример: Логирование запросов
Создайте middleware:
~~~python
class RequestLoggerMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print(f"Получен запрос: {request.method} {request.path}")
        response = self.get_response(request)
        print(f"Отправлен ответ: {response.status_code}")
        return response
~~~

---

### Настройка middleware:
Добавьте его в `MIDDLEWARE` в `settings.py`:
~~~python
MIDDLEWARE = [
    # ...
    'yourapp.middleware.RequestLoggerMiddleware',
]
~~~

---

### Пример: Кэширование ответов
~~~python
class CacheMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == 'GET':
            key = f"cache_{request.get_full_path()}"
            response = cache.get(key)
            if response is None:
                response = self.get_response(request)
                cache.set(key, response, 3600)
        else:
            response = self.get_response(request)
        return response
~~~

---

### Порядок middleware:
Порядок важен! Указывается в `MIDDLEWARE` в settings.

---

## Заключение
Вы научились создавать и настраивать middleware.

Переходите к практическим заданиям: [Tasks](../practice/tasks.md)