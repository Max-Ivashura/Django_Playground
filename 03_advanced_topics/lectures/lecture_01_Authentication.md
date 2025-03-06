# Лекция 1: Аутентификация в Django

## Введение
Django предоставляет встроенную систему аутентификации для управления пользователями. Она включает:
- Регистрацию.
- Вход/выход.
- Управление правами доступа.

---

## Основные компоненты

### 1. Модель пользователя
Django использует модель `User` из `django.contrib.auth.models`.

### 2. Встроенные views
- `LoginView` и `LogoutView` для входа/выхода.
- `PasswordChangeView`, `PasswordResetView` и другие.

### 3. Декораторы
- `@login_required`: Защита views.
- `@permission_required`: Проверка прав доступа.

---

## Пример реализации

### 1. Настройка URL
Добавьте маршруты для аутентификации в `urls.py`:
```python
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
]
```

### 2. Шаблоны
Создайте шаблоны для входа (login.html):
```html
<form method="post">
    {% csrf_token %}
    {{ form.as_p }}
    <button type="submit">Войти</button>
</form>
```
### 3. Защита views
```
from django.contrib.auth.decorators import login_required

@login_required
def secret_page(request):
    return render(request, 'secret.html')
```
### Кастомизация
Вы можете:

Изменить шаблоны аутентификации.
Добавить дополнительные поля в форму регистрации.
Настроить политики безопасности (например, минимальная длина пароля).

### Заключение
В этой лекции мы рассмотрели основы аутентификации в Django. Вы научились:

Настроить вход/выход.
Защитить views с помощью декораторов.
Использовать встроенные views и формы.
Переходите к следующей лекции: Кастомна