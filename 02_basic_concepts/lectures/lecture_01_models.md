# Лекция 1: Models

## Введение
Models в Django представляют собой классы Python, которые описывают структуру данных вашей базы данных. Они позволяют взаимодействовать с базой данных без написания SQL-запросов.

Django использует Object-Relational Mapping (ORM) для работы с базами данных.

---

## Основные концепции

### 1. Создание модели
Модели создаются в файле `models.py` приложения. Вот пример простой модели:

```python
from django.db import models

class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    published_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
```

- `title`: Поле строки с максимальной длиной 200 символов.
- `content`: Текстовое поле для хранения длинных текстов.
- `published_date`: Автоматически устанавливается при создании записи.

---

### 2. Типы полей
Django предоставляет множество типов полей. Вот некоторые из них:
- `CharField`: Для строк.
- `TextField`: Для длинных текстов.
- `IntegerField`: Для целых чисел.
- `BooleanField`: Для логических значений (`True`/`False`).
- `DateTimeField`: Для дат и времени.
- `ForeignKey`: Для связей "один-ко-многим".
- `ManyToManyField`: Для связей "многие-ко-многим".

---

### 3. Миграции
После создания или изменения модели нужно применить миграции:
1. Создайте миграции:
   ```bash
   python manage.py makemigrations
   ```
2. Примените миграции:
   ```bash
   python manage.py migrate
   ```

---

### 4. Работа с данными
Django предоставляет мощный QuerySet API для работы с данными. Вот несколько примеров:

#### Создание записи:
```python
article = Article(title="Новый статья", content="Это содержимое статьи.")
article.save()
```

#### Получение записей:
```python
articles = Article.objects.all()  # Все записи
article = Article.objects.get(id=1)  # Одна запись по ID
```

#### Фильтрация:
```python
recent_articles = Article.objects.filter(published_date__year=2023)
```

#### Обновление:
```python
article = Article.objects.get(id=1)
article.title = "Обновленный заголовок"
article.save()
```

#### Удаление:
```python
article.delete()
```

---

## Заключение

В этой лекции мы рассмотрели основы работы с моделями в Django. Вы научились:
- Создавать модели.
- Применять миграции.
- Работать с данными через ORM.

Переходите к следующей лекции: [Views](../lecture_02_Views.md)