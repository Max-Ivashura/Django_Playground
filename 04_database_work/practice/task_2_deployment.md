# Практические задания для модуля "Deployment" (BookStore)

---

## Задание 1: Настройка Production-среды

### Шаги:
1. **Создайте файл `.env`**:
   ~~~env
   DJANGO_SECRET_KEY=your-secret-key
   DB_NAME=bookstore_db
   DB_USER=bookstore_user
   DB_PASSWORD=bookstore_password
   DB_HOST=localhost
   DB_PORT=5432
   DJANGO_SETTINGS_MODULE=bookstore.settings
   ~~~

2. **Настройте `settings.py`**:
   - Импортируйте `environ`:
     ~~~python
     import os
     import environ

     env = environ.Env()
     environ.Env.read_env()
     ~~~

   - Отключите `DEBUG`:
     ~~~python
     DEBUG = False
     ~~~

   - Настройте безопасность:
     ~~~python
     ALLOWED_HOSTS = ['yourdomain.com', 'localhost']
     SECURE_SSL_REDIRECT = True
     SECURE_HSTS_SECONDS = 31536000
     ~~~

   - Настройте PostgreSQL:
     ~~~python
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

   - Настройте статику:
     ~~~python
     STATIC_URL = '/static/'
     STATIC_ROOT = BASE_DIR / 'staticfiles'
     MEDIA_URL = '/media/'
     MEDIA_ROOT = BASE_DIR / 'media'
     ~~~

3. **Настройте `manage.py`**:
   ~~~python
   import os
   import environ

   env = environ.Env()
   environ.Env.read_env()

   os.environ.setdefault('DJANGO_SETTINGS_MODULE', env('DJANGO_SETTINGS_MODULE'))
   ~~~

4. **Соберите статику**:
   ~~~bash
   python manage.py collectstatic
   ~~~

---

## Задание 2: Dockerization

### Шаги:
1. **Создайте `docker-compose.yml`**:
   ~~~yaml
   version: '3.8'

   services:
     web:
       build: .
       command: gunicorn bookstore.wsgi:application --bind 0.0.0.0:8000
       volumes:
         - .:/code
       ports:
         - "8000:8000"
       env_file:
         - .env
       depends_on:
         - db

     db:
       image: postgres:13
       volumes:
         - postgres_data:/var/lib/postgresql/data
       environment:
         - POSTGRES_DB=${DB_NAME}
         - POSTGRES_USER=${DB_USER}
         - POSTGRES_PASSWORD=${DB_PASSWORD}

   volumes:
     postgres_data:
   ~~~

2. **Создайте `Dockerfile`**:
   ~~~dockerfile
   FROM python:3.9-slim

   WORKDIR /code

   COPY requirements.txt .
   RUN pip install -r requirements.txt

   COPY . .

   CMD ["gunicorn", "bookstore.wsgi:application", "--bind", "0.0.0.0:8000"]
   ~~~

3. **Запустите Docker**:
   ~~~bash
   docker-compose up --build
   ~~~

---

## Задание 3: Деплой на сервер (Ubuntu)

### Шаги:
1. **Подготовьте сервер**:
   ~~~bash
   sudo apt update && sudo apt upgrade -y
   sudo apt install python3-pip nginx postgresql postgresql-contrib
   sudo adduser deploy_user
   sudo usermod -aG sudo deploy_user
   ~~~

2. **Настройте PostgreSQL**:
   ~~~bash
   sudo -u postgres psql
   CREATE DATABASE bookstore_db;
   CREATE USER bookstore_user WITH PASSWORD 'bookstore_password';
   GRANT ALL PRIVILEGES ON DATABASE bookstore_db TO bookstore_user;
   \q
   ~~~

3. **Настройте Nginx**:
   ~~~nginx
   # /etc/nginx/sites-available/bookstore
   server {
       listen 80;
       server_name yourdomain.com;

       location / {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
       }

       location /static/ {
           alias /path/to/your/project/staticfiles/;
       }

       location /media/ {
           alias /path/to/your/project/media/;
       }
   }
   ~~~

4. **Настройте Gunicorn через systemd**:
   ~~~ini
   # /etc/systemd/system/bookstore.service
   [Unit]
   Description=Gunicorn instance for BookStore
   After=network.target

   [Service]
   User=deploy_user
   Group=www-data
   WorkingDirectory=/path/to/your/project
   Environment="PATH=/path/to/your/project/venv/bin"
   ExecStart=/path/to/your/project/venv/bin/gunicorn bookstore.wsgi:application --bind 0.0.0.0:8000

   [Install]
   WantedBy=multi-user.target
   ~~~

5. **Запустите службу**:
   ~~~bash
   sudo systemctl enable bookstore
   sudo systemctl start bookstore
   ~~~

---

## Задание 4: Тестирование деплоя

### Шаги:
1. **Проверьте доступ через браузер**:
   - Откройте `http://yourdomain.com`.

2. **Тестирование загрузки медиа-файлов**:
   - Убедитесь, что обложки книг отображаются корректно.

3. **Настройка HTTPS**:
   ~~~bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx -d yourdomain.com
   ~~~

---

## Критерии успеха:
1. **Задание 1**:
   - `.env` содержит все переменные.
   - Статика собрана в `staticfiles/`.

2. **Задание 2**:
   - Приложение работает через Docker.

3. **Задание 3**:
   - Каталог книг доступен по доменному имени.
   - Медиа-файлы (обложки) отображаются.

---

### **Структура проекта**:
```
bookstore/
├── books/          # Приложение
├── .env
├── docker-compose.yml
├── Dockerfile
├── requirements.txt  # Содержит django, gunicorn, psycopg2-binary
├── settings.py
└── manage.py
```

---

### **Пример `requirements.txt`**:
```
django
gunicorn
psycopg2-binary
python-dotenv
Pillow  # Для обработки изображений
```

---

### **Что делать если возникли ошибки?**
- **Ошибка подключения к БД**:
  - Проверьте переменные в `.env`.
  - Убедитесь, что PostgreSQL запущен.

- **Ошибка медиа-файлов**:
  - Проверьте путь `MEDIA_ROOT` в `settings.py`.
  - Настройте Nginx для `/media/`.

---

### **Проверьте через:**
1. **Docker**:
   ~~~bash
   docker-compose up --build
   ~~~

2. **Сервер**:
   - Убедитесь, что обложки книг загружаются через Nginx.

---
