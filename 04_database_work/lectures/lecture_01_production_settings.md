# Лекция 1: Настройка Production-среды

## Введение
Для безопасного развертывания Django-приложения в production (рабочей среде) необходимо:
- Отключить отладочные режимы.
- Использовать безопасные настройки.
- Настроить работу с базой данных и статикой.

---

### **1. Переменные окружения**
**Зачем?**  
Секретные данные (пароли, ключи) не должны храниться в коде. Используйте файл `.env`.

#### **Как это сделать?**
1. **Создайте файл `.env`**:
   ~~~env
   DJANGO_SECRET_KEY=your-secret-key  # Генерируется через `python -c 'from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())'`
   DB_NAME=your_db_name
   DB_USER=your_db_user
   DB_PASSWORD=your_db_password
   DB_HOST=localhost
   DB_PORT=5432
   ~~~

2. **Добавьте библиотеку для загрузки `.env`**:
   ~~~bash
   pip install python-dotenv
   ~~~

3. **Импортируйте переменные в `manage.py`**:
   ~~~python
   # manage.py
   import os
   import environ

   env = environ.Env()
   environ.Env.read_env()  # Загрузка .env

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', env('DJANGO_SETTINGS_MODULE'))
   ~~~

---

### **2. Безопасные настройки в `settings.py`**
**Зачем?**  
Для защиты от атак и улучшения безопасности.

#### **Пример настроек**:
- **Отключите отладку**:
  ~~~python
  DEBUG = False
  ~~~

- **Разрешите домены**:
  ~~~python
  ALLOWED_HOSTS = ['yourdomain.com', 'localhost']
  ~~~

- **Настройки HTTPS**:
  ~~~python
  SECURE_SSL_REDIRECT = True  # Перенаправление на HTTPS
  SECURE_HSTS_SECONDS = 31536000  # Время действия заголовка HSTS
  SECURE_CONTENT_TYPE_NOSNIFF = True  # Защита от MIME-sniffing
  CSRF_COOKIE_SECURE = True  # Cookies только через HTTPS
  ~~~

---

### **3. Настройка базы данных**
**Зачем?**  
PostgreSQL более надежен и масштабируем, чем SQLite.

#### **Пример настроек для PostgreSQL**:
~~~
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME'),
        'USER': os.environ.get('DB_USER'),
        'PASSWORD': os.environ.get('DB_PASSWORD'),
        'HOST': os.environ.get('DB_HOST', 'localhost'),
        'PORT': os.environ.get('DB_PORT', '5432'),
    }
}
~~~

---

### **4. Статика и медиа-файлы**
**Зачем?**  
В production Django не обслуживает статику напрямую — это делает Nginx.

#### **Настройки в `settings.py`**:
- **Статика**:
  ~~~python
  STATIC_URL = '/static/'
  STATIC_ROOT = BASE_DIR / 'staticfiles'  # Папка для сборки статики
  ~~~

- **Медиа** (например, аватарки):
  ~~~python
  MEDIA_URL = '/media/'
  MEDIA_ROOT = BASE_DIR / 'media'  # Папка для медиа-файлов
  ~~~

#### **Сборка статики**:
~~~
python manage.py collectstatic
~~~

---

### **5. Зависимости**
**Какие пакеты нужны?**
- `gunicorn` — веб-сервер для Python.
- `psycopg2-binary` — драйвер для PostgreSQL.

Добавьте их в `requirements.txt`:
~~~
django
gunicorn
psycopg2-binary
python-dotenv
~~~

---

### **Что делаем в этой лекции?**
1. Настроим `.env` и безопасные настройки.
2. Подготовим базу данных.
3. Настроим сборку статики.

---

### **Проверка**:
1. Убедитесь, что `DEBUG = False`.
2. Проверьте подключение к PostgreSQL:
   ~~~bash
   python manage.py check
   ~~~

3. Соберите статику:
   ~~~bash
   python manage.py collectstatic
   ~~~

---

### **Следующий шаг**:
Перейдем к Docker-настройкам (лекция 2).