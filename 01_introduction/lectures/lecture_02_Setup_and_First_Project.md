# Лекция 2: Установка и создание первого проекта

## Введение
В этой лекции мы научимся устанавливать Django и создавать свой первый проект. Мы также рассмотрим основные команды, которые будут использоваться на протяжении всего курса.

---

## 1. Подготовка среды разработки

### 1.1 Проверка Python
Убедитесь, что у вас установлен Python 3.8 или выше. Вы можете проверить версию Python, выполнив следующую команду в терминале:

~~~bash
python --version
# или
python3 --version
~~~

Если Python не установлен, вы можете скачать его с официального сайта: [https://www.python.org/downloads/](https://www.python.org/downloads/).

---

### 1.2 Создание virtual environment
Для изоляции зависимостей вашего проекта рекомендуется использовать виртуальное окружение. Создайте новое виртуальное окружение:

~~~bash
python -m venv venv
# или для Linux/Mac:
python3 -m venv venv
~~~

Активируйте виртуальное окружение:

- Для Linux/Mac:
  ~~~bash
  source venv/bin/activate
  ~~~

- Для Windows:
  ~~~bash
  venv\Scripts\activate
  ~~~

Теперь все команды pip будут работать только внутри этого виртуального окружения.

---

## 2. Установка Django

Установите Django с помощью pip:

~~~bash
pip install django
~~~

Проверьте успешность установки:

~~~bash
django-admin --version
~~~

Вы должны увидеть номер версии Django, например, `4.1.7`.

---

## 3. Создание первого проекта

### 3.1 Создание проекта
Создайте новый проект Django с помощью команды `django-admin`:

~~~bash
django-admin startproject mysite
~~~

Это создаст директорию `mysite` с базовой структурой проекта.

Структура проекта будет выглядеть так:

~~~
mysite/
├── manage.py
├── mysite/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── asgi.py
│   └── wsgi.py
~~~

- `manage.py`: Скрипт для управления проектом.
- `settings.py`: Настройки проекта.
- `urls.py`: Конфигурация URL-маршрутизации.
- `asgi.py` и `wsgi.py`: Настройки для запуска приложения в production.

---

### 3.2 Запуск сервера разработки
Перейдите в директорию проекта:

~~~bash
cd mysite
~~~

Запустите локальный сервер разработки:

~~~bash
python manage.py runserver
~~~

По умолчанию сервер будет доступен по адресу [http://127.0.0.1:8000/](http://127.0.0.1:8000/). Откройте этот адрес в браузере, и вы увидите приветственную страницу Django.

---

## 4. Создание первого приложения

В Django проект состоит из одного или нескольких приложений. Создадим первое приложение:

~~~bash
python manage.py startapp hello_world
~~~

Это создаст директорию `hello_world` с базовой структурой приложения:

~~~
hello_world/
├── admin.py
├── apps.py
├── migrations/
├── models.py
├── tests.py
└── views.py
~~~

---

### 4.1 Регистрация приложения
Откройте файл `mysite/settings.py` и добавьте `'hello_world'` в список `INSTALLED_APPS`:

~~~python
INSTALLED_APPS = [
    # ...
    'hello_world',
]
~~~

---

### 4.2 Создание первой View
Откройте файл `hello_world/views.py` и добавьте следующий код:

~~~python
from django.http import HttpResponse

def hello(request):
    return HttpResponse("Hello, Django!")
~~~

---

### 4.3 Настройка URL
Откройте файл `mysite/urls.py` и импортируйте функцию `hello`:

~~~python
from django.urls import path
from hello_world import views

urlpatterns = [
    path('hello/', views.hello, name='hello'),
]
~~~

---

### 4.4 Проверка работы
Остановите сервер (Ctrl+C) и запустите его снова:

~~~bash
python manage.py runserver
~~~

Перейдите по адресу [http://127.0.0.1:8000/hello/](http://127.0.0.1:8000/hello/) и вы увидите сообщение "Hello, Django!".

---

## Заключение

В этой лекции мы:
1. Установили Django.
2. Создали первый проект.
3. Создали первое приложение.
4. Реализовали простую View и настроили маршрутизацию.

Переходите к практическим заданиям: [Практические задания](../practice/tasks.md)