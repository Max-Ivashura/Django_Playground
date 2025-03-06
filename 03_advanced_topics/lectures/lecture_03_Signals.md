# Лекция 3: Signals

## Введение
Signals позволяют выполнять действия при определенных событиях.

---

### Пример: Логирование создания пользователя
1. **Создайте сигнал**:
   ~~~python
   from django.db.models.signals import post_save
   from django.dispatch import receiver
   from django.contrib.auth.models import User

   @receiver(post_save, sender=User)
   def log_user_creation(sender, instance, created, **kwargs):
       if created:
           print(f"Пользователь {instance.username} создан")
   ~~~

2. **Подключите сигнал**:
   Добавьте `import` в `apps.py` вашего приложения:
   ~~~python
   from .signals import *
   ~~~

---

### Доступные сигналы:
- `pre_save`, `post_save`
- `pre_delete`, `post_delete`
- `request_started`, `request_finished`

---

### Создайте собственный сигнал:
~~~python
from django.dispatch import Signal

user_registered = Signal(providing_args=['user', 'request'])

def send_welcome_email(sender, user, request, **kwargs):
    # Логика отправки письма

user_registered.connect(send_welcome_email)
~~~

---

## Заключение
Signals позволяют декларативно реагировать на события.

Переходите к следующей лекции: [Middleware](../lecture_04_Middleware.md)