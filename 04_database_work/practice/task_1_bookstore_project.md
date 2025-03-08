# Проект "BookStore": Интернет-магазин книг

---

## Цель проекта:
Создать приложение для управления каталогом книг и их продажей.

---

## Шаги по созданию проекта:

### **1. Создайте проект и приложение**
```bash
django-admin startproject bookstore
cd bookstore
python manage.py startapp books
```

### **2. Настройте модель книги**
**Файл: `books/models.py`**
```python
from django.db import models

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    stock = models.IntegerField()
    cover = models.ImageField(upload_to='covers/')

    def __str__(self):
        return self.title
```

### **3. Создайте форму для добавления книг**
**Файл: `books/forms.py`**
```python
from django import forms
from .models import Book

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'price', 'description', 'stock', 'cover']
```

### **4. Создайте view для списка книг**
**Файл: `books/views.py`**
```python
from django.shortcuts import render
from .models import Book

def book_list(request):
    books = Book.objects.all()
    return render(request, 'books/book_list.html', {'books': books})
```

### **5. Настройте URL-маршруты**
**Файл: `books/urls.py`**
```python
from django.urls import path
from . import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
]
```

### **6. Создайте шаблон для списка книг**
**Файл: `templates/books/book_list.html`**
```html
{% extends 'base.html' %}

{% block content %}
  <h1>Каталог книг</h1>
  <ul>
    {% for book in books %}
      <li>
        {{ book.title }} — ${{ book.price }}
        <img src="{{ book.cover.url }}" width="100">
      </li>
    {% empty %}
      <li>Нет книг в каталоге.</li>
    {% endfor %}
  </ul>
{% endblock %}
```

### **7. Подключите приложение в `urls.py`**
**Файл: `bookstore/urls.py`**
```python
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
]
```

### **8. Запустите сервер**
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```

---
