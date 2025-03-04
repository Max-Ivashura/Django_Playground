# Лекция 3: Templates

## Введение
Шаблоны в Django позволяют создавать динамические HTML-страницы. Они используют специальный синтаксис для встраивания данных из views в HTML.

---

## Основные концепции

### 1. Создание шаблонов

Шаблоны обычно хранятся в папке `templates` внутри приложения. Например:
```
myapp/
├── templates/
│ └── myapp/
│ └── home.html
```


---

### 2. Синтаксис шаблонизатора

Django предоставляет простой синтаксис для работы с данными:

- **Вывод переменных**: `{{ variable_name }}`
- **Циклы**: `{% for item in items %} ... {% endfor %}`
- **Условия**: `{% if condition %} ... {% endif %}`

---

### 3. Пример шаблона

Пример шаблона `home.html`:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Главная страница</title>
</head>
<body>
    <h1>{{ title }}</h1>
    <p>{{ content }}</p>

    <h2>Список статей:</h2>
    <ul>
        {% for article in articles %}
            <li>{{ article.title }} ({{ article.published_date|date:"Y-m-d" }})</li>
        {% empty %}
            <li>Нет статей.</li>
        {% endfor %}
    </ul>
</body>
</html>
```

---

### 4. Наследование шаблонов

Django поддерживает наследование шаблонов, что позволяет избежать дублирования кода. Пример:

#### Базовый шаблон (`base.html`):
```html
<!DOCTYPE html>
<html>
<head>
    <title>{% block title %}Мой сайт{% endblock %}</title>
</head>
<body>
    <header>
        <h1>Мой сайт</h1>
    </header>
    <main>
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

#### Дочерний шаблон (`home.html`):
```html
{% extends "base.html" %}

{% block title %}Главная страница{% endblock %}

{% block content %}
<h1>Добро пожаловать!</h1>
<p>Это главная страница моего сайта.</p>
{% endblock %}
```

---

## Заключение

В этой лекции мы рассмотрели основы работы с шаблонами в Django. Вы научились:
- Создавать шаблоны.
- Использовать синтаксис шаблонизатора.
- Применять наследование шаблонов.

Переходите к следующей лекции: [URLs](../lecture_04_URLs.md)