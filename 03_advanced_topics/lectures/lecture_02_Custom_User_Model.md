# Лекция 2: Кастомная модель пользователя

## Введение
По умолчанию Django использует `User`, но вы можете создать свою модель.

---

### Шаги:
1. **Создайте модель**:
   ~~~python
   from django.contrib.auth.models import AbstractUser

   class CustomUser(AbstractUser):
       phone = models.CharField(max_length=15)
       avatar = models.ImageField(upload_to='avatars/')
   ~~~

2. **Настройте settings.py**:
   ~~~python
   AUTH_USER_MODEL = 'yourapp.CustomUser'
   ~~~

3. **Создайте суперпользователя**:
   ~~~bash
   python manage.py createsuperuser
   ~~~

---

### Пример: Форма для кастомной модели:
~~~python
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'phone']
~~~

---

### Использование в views:
~~~python
from django.contrib.auth import login
from .forms import CustomUserCreationForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})
~~~

---

## Заключение
Вы создали кастомную модель пользователя и научились работать с ней.

Переходите к следующей лекции: [Signals](../lecture_03_Signals.md)