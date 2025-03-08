# Лекция 3: Процесс деплоя на сервер

## Введение
Деплой — это развертывание приложения на production-сервере (например, VPS).

---

### **1. Подготовка сервера (Ubuntu)**
**Как это сделать?**  
Установите необходимые пакеты и создайте пользователя.

#### **Шаги**:
1. **Обновите систему**:
   ~~~bash
   sudo apt update && sudo apt upgrade -y
   ~~~

2. **Установите зависимости**:
   ~~~bash
   sudo apt install python3-pip nginx postgresql postgresql-contrib
   ~~~

3. **Создайте пользователя для приложения**:
   ~~~bash
   sudo adduser deploy_user
   sudo usermod -aG sudo deploy_user
   ~~~

---

### **2. Настройка PostgreSQL**
**Как это сделать?**  
Создайте базу данных и пользователя.

#### **Команды**:
~~~
sudo -u postgres psql
CREATE DATABASE fitness_db;
CREATE USER fitness_user WITH PASSWORD 'fitness_password';
ALTER USER fitness_user WITH SUPERUSER;  # Только для тестирования!
GRANT ALL PRIVILEGES ON DATABASE fitness_db TO fitness_user;
\q
~~~

---

### **3. Настройка Nginx**
**Зачем?**  
Nginx:
- Отдает статику.
- Перенаправляет запросы в Gunicorn.

#### **Шаги**:
1. **Создайте конфигурационный файл**:
   ~~~bash
   sudo nano /etc/nginx/sites-available/fitness_tracker
   ~~~

2. **Содержимое файла**:
   ~~~nginx
   server {
       listen 80;
       server_name yourdomain.com;  # Ваш домен

       location / {
           proxy_pass http://localhost:8000;  # Перенаправление в Gunicorn
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }

       location /static/ {
           alias /path/to/your/project/staticfiles/;  # Путь к статике
       }
   }
   ~~~

3. **Активируйте конфигурацию**:
   ~~~bash
   sudo ln -s /etc/nginx/sites-available/fitness_tracker /etc/nginx/sites-enabled/
   sudo nginx -t  # Проверка настроек
   sudo systemctl restart nginx
   ~~~

---

### **4. Запуск через Gunicorn**
**Зачем?**  
Gunicorn обрабатывает HTTP-запросы от Nginx.

#### **Настройка systemd-службы**:
1. **Создайте файл службы**:
   ~~~bash
   sudo nano /etc/systemd/system/fitness.service
   ~~~

2. **Содержимое файла**:
   ~~~ini
   [Unit]
   Description=Gunicorn instance for Fitness Tracker
   After=network.target

   [Service]
   User=deploy_user  # Пользователь, от которого запускается сервис
   Group=www-data
   WorkingDirectory=/path/to/your/project
   ExecStart=/path/to/venv/bin/gunicorn fitness.wsgi:application --bind 0.0.0.0:8000

   [Install]
   WantedBy=multi-user.target
   ~~~

3. **Запуск службы**:
   ~~~bash
   sudo systemctl enable fitness.service
   sudo systemctl start fitness.service
   ~~~

---

### **5. Сборка статики**
**Как это сделать?**
~~~
python manage.py collectstatic
~~~

---

### **Что делаем в этой лекции?**
1. Настроим сервер Ubuntu.
2. Подготовим PostgreSQL и Nginx.
3. Запустим приложение через Gunicorn.

---

### **Проверка**:
1. Перейдите по доменному имени (например, `http://yourdomain.com`).
2. Убедитесь, что статика работает.
3. Проверьте подключение к базе данных.

---

### **Типичные ошибки и решения**:
- **Ошибка подключения к БД**:
  - Убедитесь, что `DATABASES` в `settings.py` указывает на правильный хост и порт.
- **Ошибка статики**:
  - Укажите правильный `STATIC_ROOT` в `nginx.conf`.
- **Ошибка Gunicorn**:
  - Проверьте права доступа к папке проекта.
  - Убедитесь, что виртуальное окружение указано в `ExecStart`.

---

### **Дополнительные шаги**:
- Настройте **HTTPS** через Let's Encrypt.
- Используйте **Celery** для асинхронных задач (изучите в следующих модулях).

---

### **Итог**
Теперь вы знаете:
- Как настроить безопасные настройки.
- Как использовать Docker для разработки.
- Как развернуть приложение на сервере.

Если возникнут вопросы, спрашивайте! 😊