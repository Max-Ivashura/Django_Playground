# Лекция 2: Dockerization

## Введение
Docker — это инструмент для создания изолированных окружений. Это упрощает:
- Тестирование.
- Развертывание на разных серверах.

---

### **1. Файл `docker-compose.yml`**
**Что это?**  
Определяет сервисы (веб-приложение и база данных) и их настройки.

#### **Структура файла**:
~~~
version: '3.8'

services:
  web:  # Наш Django-сервис
    build: .  # Построить образ из текущей папки
    command: gunicorn your_project.wsgi:application --bind 0.0.0.0:8000
    volumes:
      - .:/code  # Синхронизация кода между хостом и контейнером
    ports:
      - "8000:8000"  # Маппинг портов
    env_file:
      - .env  # Используем переменные из .env
    depends_on:
      - db  # Зависимость от базы данных

  db:  # Сервис базы данных
    image: postgres:13  # Используем официальный образ PostgreSQL
    volumes:
      - postgres_data:/var/lib/postgresql/data  # Постоянное хранение данных БД
    environment:
      - POSTGRES_DB=your_db  # Название БД
      - POSTGRES_USER=your_user  # Пользователь БД
      - POSTGRES_PASSWORD=your_password  # Пароль пользователя

volumes:
  postgres_data:  # Объявление тома для хранения данных БД
~~~

---

### **2. Файл `Dockerfile`**
**Зачем?**  
Определяет шаги по созданию образа для вашего приложения.

#### **Структура файла**:
~~~
FROM python:3.9-slim  # Основной образ

WORKDIR /code  # Рабочая директория в контейнере

COPY requirements.txt .  # Копируем список зависимостей
RUN pip install -r requirements.txt  # Устанавливаем зависимости

COPY . .  # Копируем весь код в контейнер

CMD ["gunicorn", "your_project.wsgi:application", "--bind", "0.0.0.0:8000"]
  # Запуск через Gunicorn
~~~

---

### **3. Запуск через Docker Compose**
**Как это работает?**  
Docker Compose создает и управляет контейнерами.

#### **Команды**:
- **Построить образы и запустить контейнеры**:
  ~~~bash
  docker-compose up --build
  ~~~

- **Запустить в фоновом режиме**:
  ~~~bash
  docker-compose up -d
  ~~~

- **Остановить контейнеры**:
  ~~~bash
  docker-compose down
  ~~~

---

### **4. Тестирование Docker-контейнера**
1. Запустите контейнеры:
   ~~~bash
   docker-compose up --build
   ~~~

2. Откройте `http://localhost:8000` в браузере.

---

### **Что делаем в этой лекции?**
1. Создадим `docker-compose.yml` и `Dockerfile`.
2. Запустим приложение в Docker.
3. Убедимся, что все работает локально.

---

### **Пример для Fitness Tracker**:
**Файл `docker-compose.yml`**:
~~~
version: '3.8'

services:
  web:
    build: .
    command: gunicorn fitness_tracker.wsgi:application --bind 0.0.0.0:8000
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
      - POSTGRES_DB=fitness_db
      - POSTGRES_USER=fitness_user
      - POSTGRES_PASSWORD=fitness_password

volumes:
  postgres_data:
~~~

---

### **Проверка**:
1. Запустите Docker:
   ~~~bash
   docker-compose up --build
   ~~~

2. Проверьте через `http://localhost:8000`.

---

### **Следующий шаг**:
Настроим деплой на сервер (лекция 3).