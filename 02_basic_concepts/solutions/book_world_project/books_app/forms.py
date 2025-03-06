from django import forms
from .models import Book, Comment


class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'published_date', 'price']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class RatingForm(forms.Form):
    rating = forms.IntegerField(min_value=1, max_value=5)

class SearchForm(forms.Form):
    query = forms.CharField(label='Search', required=False)