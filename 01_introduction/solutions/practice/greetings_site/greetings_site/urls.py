from django.contrib import admin
from django.urls import path
from greetings import views

urlpatterns = [
    path('greet/<str:name>/', views.greet_user, name='greet_user'),
    path('admin/', admin.site.urls),
]
