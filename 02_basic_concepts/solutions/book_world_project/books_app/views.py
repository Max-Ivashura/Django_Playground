from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from .models import Book
from .forms import BookForm, CommentForm, RatingForm, SearchForm  # Мы создадим форму позже

# Список всех книг
def book_list(request):
    form = SearchForm(request.GET)
    books = Book.objects.all()

    if form.is_valid():
        query = form.cleaned_data.get('query')
        if query:
            books = books.filter(title__icontains=query) | books.filter(author__icontains=query)

    paginator = Paginator(books, 10)  # 10 книг на страницу
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'book_list.html', {'page_obj': page_obj, 'form': form})


def book_detail(request, id):
    book = get_object_or_404(Book, id=id)
    comments = book.comments.all()

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.user = request.user
            comment.save()
            return redirect('book_detail', id=book.id)
    else:
        form = CommentForm()

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        if rating_form.is_valid():
            rating = rating_form.cleaned_data['rating']
            book.rating = (book.rating + rating) / 2  # Простое среднее значение
            book.save()
            return redirect('book_detail', id=book.id)
    else:
        rating_form = RatingForm()

    return render(request, 'book_detail.html', {
        'book': book,
        'comments': comments,
        'form': form,
        'rating_form': rating_form
    })

@login_required
def book_create(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'book_create.html', {'form': form})


def book_update(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'POST':
        form = BookForm(request.POST, instance=book)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm(instance=book)
    return render(request, 'book_update.html', {'form': form})


def book_delete(request, id):
    book = get_object_or_404(Book, pk=id)
    if request.method == 'POST':
        book.delete()
        return redirect('book_list')
    return render(request, 'book_delete.html', {'book': book})
