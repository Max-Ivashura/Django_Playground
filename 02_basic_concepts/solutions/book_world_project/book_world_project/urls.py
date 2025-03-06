from django.contrib.auth import views as auth_views
from django.urls import path
from books_app import views

urlpatterns = [
    path('', views.book_list, name='book_list'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('<int:id>/', views.book_detail, name='book_detail'),
    path('create/', views.book_create, name='book_create'),
    path('<int:id>/update/', views.book_update, name='book_update'),
    path('<int:id>/delete/', views.book_delete, name='book_delete'),
]
