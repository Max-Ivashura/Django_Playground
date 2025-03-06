Задания для модуля **Advanced Topics** на тему **"Fitness Tracker"** (приложения для отслеживания тренировок), которые вы будете реализовывать **последовательно**, начиная с создания проекта:

---

# Практические задания для модуля "Advanced Topics" (Fitness Tracker)

---

## Задание 1: Создание проекта и приложения

**Цель**: Создать проект и приложение для трекера фитнес-данных.

### Инструкции:
1. Создайте новый проект:
   ```bash
   django-admin startproject fitness_tracker
   cd fitness_tracker
   ```

2. Создайте приложение:
   ```bash
   python manage.py startapp workouts
   ```

---

## Задание 2: Кастомная модель пользователя

**Цель**: Создать модель пользователя с ролями (admin, trainer, client) и дополнительными полями.

### Инструкции:
1. **Создайте модель `User`**:
   - Наследуйте от `AbstractUser`.
   - Добавьте поле `role` (choices: admin, trainer, client).
   - Добавьте поле `age` (число) и `weight` (число с плавающей точкой).

   Пример:
   ~~~python
   from django.contrib.auth.models import AbstractUser

   class User(AbstractUser):
       ROLE_CHOICES = (
           ('admin', 'Администратор'),
           ('trainer', 'Тренер'),
           ('client', 'Клиент'),
       )
       role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='client')
       age = models.IntegerField(null=True)
       weight = models.DecimalField(max_digits=5, decimal_places=1, null=True)
   ~~~

2. **Настройте проект**:
   - Укажите `AUTH_USER_MODEL = 'workouts.User'` в `settings.py`.
   - Создайте миграции и примените их:
     ```bash
     python manage.py makemigrations
     python manage.py migrate
     ```

3. **Создайте суперпользователя**:
   ```bash
   python manage.py createsuperuser
   ```

---

## Задание 3: Модель тренировки

**Цель**: Создать модель `Workout` для отслеживания тренировок.

### Инструкции:
1. **Создайте модель**:
   ~~~python
   class Workout(models.Model):
       name = models.CharField(max_length=100)
       duration = models.IntegerField(help_text='В минутах')
       calories_burned = models.IntegerField()
       user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workouts')
       created_at = models.DateTimeField(auto_now_add=True)
   ~~~

2. **Примените миграции**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

---

## Задание 4: Форма регистрации

**Цель**: Реализовать форму регистрации с выбором роли и валидацией данных.

### Инструкции:
1. **Создайте форму**:
   ~~~python
   from django import forms
   from .models import User

   class CustomUserCreationForm(forms.ModelForm):
       password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
       password2 = forms.CharField(label='Confirm Password', widget=forms.PasswordInput)

       class Meta:
           model = User
           fields = ['username', 'email', 'role', 'age', 'weight']

       def clean_password2(self):
           # Ваш код для проверки паролей
           pass

       def save(self, commit=True):
           # Ваш код для сохранения пользователя
           pass
   ~~~

2. **Создайте view для регистрации**:
   ~~~python
   def register(request):
       # Ваш код для обработки формы
       pass
   ~~~

3. **Настройте URL**:
   ~~~python
   path('register/', views.register, name='register'),
   ~~~

---

## Задание 5: Signals для логирования тренировок

**Цель**: Отправить email админу при создании новой тренировки.

### Инструкции:
1. **Создайте signal**:
   ~~~python
   from django.db.models.signals import post_save
   from django.dispatch import receiver
   from .models import Workout

   @receiver(post_save, sender=Workout)
   def notify_admin_on_workout(sender, instance, created, **kwargs):
       if created:
           # Ваш код для отправки email через send_mail
           pass
   ~~~

2. **Подключите signal**:
   - В файле `apps.py`:
     ~~~python
     class WorkoutsConfig(AppConfig):
         def ready(self):
             import workouts.signals
     ~~~

---

## Задание 6: Middleware для логирования времени и блокировки IP

**Цель**: Создать middleware, который:
- Логирует время обработки запросов.
- Блокирует доступ для запрещенных IP-адресов.

### Инструкции:
1. **Middleware для логирования времени**:
   ~~~python
   import time

   class RequestTimeMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           start_time = time.time()
           response = self.get_response(request)
           duration = time.time() - start_time
           print(f"Запрос {request.path} обработан за {duration:.2f} сек.")
           return response
   ~~~

2. **Middleware для блокировки IP**:
   - В `settings.py` добавьте список `BLOCKED_IPS`.
   ~~~python
   class BlockIPMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           # Ваш код для проверки IP-адреса
           return self.get_response(request)
   ~~~

3. **Настройте middleware в settings.py**:
   ~~~python
   MIDDLEWARE = [
       # ...
       'fitness_tracker.middleware.RequestTimeMiddleware',
       'fitness_tracker.middleware.BlockIPMiddleware',
   ]
   ~~~

---

## Задание 7: Аутентификация и доступ к тренировкам

**Цель**: Создать view для просмотра списка тренировок, доступный только авторизованным пользователям.

### Инструкции:
1. **View для списка тренировок**:
   ~~~python
   from django.contrib.auth.decorators import login_required

   @login_required
   def workout_list(request):
       workouts = Workout.objects.filter(user=request.user)
       return render(request, 'workouts/workout_list.html', {'workouts': workouts})
   ~~~

2. **URL для view**:
   ~~~python
   path('workouts/', views.workout_list, name='workout_list'),
   ~~~

3. **Шаблон `workout_list.html`**:
   ~~~html
   <h1>Ваши тренировки</h1>
   <ul>
       {% for workout in workouts %}
           <li>{{ workout.name }} — {{ workout.duration }} мин.</li>
       {% empty %}
           <li>Нет тренировок.</li>
       {% endfor %}
   </ul>
   ~~~

---

## Задание 8: Права доступа для админов

**Цель**: Создать view админ-панели для управления тренировками.

### Инструкции:
1. **View админ-панели**:
   ~~~python
   from django.contrib.auth.decorators import user_passes_test

   @user_passes_test(lambda u: u.role == 'admin')
   def admin_dashboard(request):
       all_workouts = Workout.objects.all()
       return render(request, 'workouts/admin_dashboard.html', {'workouts': all_workouts})
   ~~~

2. **URL для админ-панели**:
   ~~~python
   path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
   ~~~

---

## Задание 9: Админ-панель для моделей

**Цель**: Настроить админ-панель для моделей `User` и `Workout`.

### Инструкции:
1. **Админ-панель для User**:
   ~~~python
   from django.contrib import admin
   from django.contrib.auth.admin import UserAdmin
   from .models import User

   @admin.register(User)
   class CustomUserAdmin(UserAdmin):
       list_display = ('username', 'role', 'age', 'weight')
   ~~~

2. **Админ-панель для Workout**:
   ~~~python
   @admin.register(Workout)
   class WorkoutAdmin(admin.ModelAdmin):
       list_display = ('name', 'duration', 'calories_burned', 'user', 'created_at')
   ~~~

---

## Задание 10: Middleware для сжатия ответов

**Цель**: Реализовать middleware, который сжимает ответы через `gzip`.

### Инструкции:
1. **Создайте middleware**:
   ~~~python
   import gzip

   class GZipMiddleware:
       def __init__(self, get_response):
           self.get_response = get_response

       def __call__(self, request):
           response = self.get_response(request)
           # Ваш код для сжатия ответа
           return response
   ~~~

2. **Добавьте middleware в settings.py**:
   ~~~python
   MIDDLEWARE = [
       # ...
       'fitness_tracker.middleware.GZipMiddleware',
   ]
   ~~~

---

## Задание 11: Форма создания тренировки

**Цель**: Создать форму для добавления новой тренировки.

### Инструкции:
1. **Форма для Workout**:
   ~~~python
   class WorkoutForm(forms.ModelForm):
       class Meta:
           model = Workout
           fields = ['name', 'duration', 'calories_burned']
   ~~~

2. **View для добавления тренировки**:
   ~~~python
   @login_required
   def add_workout(request):
       if request.method == 'POST':
           form = WorkoutForm(request.POST)
           if form.is_valid():
               workout = form.save(commit=False)
               workout.user = request.user
               workout.save()
               return redirect('workout_list')
       else:
           form = WorkoutForm()
       return render(request, 'workouts/add_workout.html', {'form': form})
   ~~~

3. **Шаблон `add_workout.html`**:
   ~~~html
   <form method="post">
       {% csrf_token %}
       {{ form.as_p }}
       <button>Создать тренировку</button>
   </form>
   ~~~

---

## Задание 12: Проверка ролей в шаблонах

**Цель**: Отображать элементы только для админов/тренеров.

### Инструкции:
1. **В шаблоне `base.html`**:
   ~~~html
   {% if user.is_authenticated %}
       {% if user.role == 'admin' %}
           <a href="{% url 'admin_dashboard' %}">Админ-панель</a>
       {% endif %}
   {% endif %}
   ~~~

---

## Проверка работы:
1. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

2. Проверьте:
   - Регистрацию через `/register/`.
   - Создание тренировки через форму.
   - Логирование времени запросов в консоли.
   - Блокировку доступа для запрещенных IP.
   - Доступ админов к `/admin-dashboard/`.

---

### **Структура проекта**:
```
fitness_tracker/
├── workouts/
│   ├── models.py      # User, Workout
│   ├── forms.py       # CustomUserCreationForm, WorkoutForm
│   ├── views.py       # register, workout_list, add_workout, admin_dashboard
│   ├── signals.py     # notify_admin_on_workout
│   ├── apps.py        # Подключение signals
│   ├── middleware.py  # RequestTimeMiddleware, BlockIPMiddleware, GZipMiddleware
│   └── urls.py        # Настройка маршрутов
├── settings.py        # Настройки middleware, auth, email
└── templates/
    ├── register.html  # Форма регистрации
    ├── workout_list.html  # Список тренировок
    └── add_workout.html  # Форма добавления тренировки
```

---

### **Критерии успеха**:
1. Пользователи могут регистрироваться и создавать тренировки.
2. Админы видят админ-панель и получают уведомления о новых тренировках.
3. Middleware логирует время, блокирует IP и сжимает ответы.
4. Только авторизованные пользователи видят свои тренировки.

---

### **Подсказки**:
- **Для signals**:
  - Используйте `send_mail()` из `django.core.mail`.
  - Укажите `from_email` и список `recipient_list` в настройках.

- **Для middleware**:
  - Для блокировки IP проверяйте `request.META['REMOTE_ADDR']`.

- **Для аутентификации**:
  - Используйте декораторы `login_required` и `user_passes_test`.

---

### **Проверьте через**:
1. Админ-панель (`/admin/`):
   - Добавьте тренировку через админку.
   - Убедитесь, что сигнал отправляет email.

2. Веб-интерфейс:
   - Зарегистрируйтесь как клиент и создайте тренировку.
   - Проверьте, что админ видит все тренировки на `/admin-dashboard/`.

3. Консоль:
   - Убедитесь, что middleware выводит время запросов.

---

Удачи! 🏋️ Если возникнут вопросы, вспомните:
- Лекции по **Custom User Model**, **Signals**, **Middleware**.
- Официальную документацию Django.


---

### **Порядок выполнения**:
1. Создайте проект и приложение (`workouts`).
2. Реализуйте **Задание 2** (кастомную модель пользователя).
3. Реализуйте **Задание 3** (модель тренировки).
4. Реализуйте **Задание 4** (форму регистрации).
5. Реализуйте **Задание 5** (signal для уведомлений).
6. Реализуйте **Задание 6** (middleware для логирования и блокировки).
7. Реализуйте **Задание 7** (view списка тренировок).
8. Реализуйте **Задание 8** (view админ-панели).
9. Реализуйте **Задание 9** (настройку админ-панели).
10. Реализуйте **Задание 10** (middleware для сжатия).
11. Реализуйте **Задание 11** (форму добавления тренировки).
12. Реализуйте **Задание 12** (условия в шаблонах).

---

Этот проект поможет вам закрепить все продвинутые темы! 💪 Если что-то не работает, проверьте:
- Настройку `AUTH_USER_MODEL`.
- Импорты моделей в файлах signals и forms.
- Порядок middleware в `settings.py`.