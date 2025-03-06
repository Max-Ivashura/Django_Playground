from django.shortcuts import render
from .models import Person


def greet_user(request, name):
    # Получаем всех пользователей из базы данных
    people = Person.objects.all()

    return render(request, 'greet.html', {
        'name': name,
        'users': people
    })
