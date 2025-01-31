from django import forms
from .models import Review, Album

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['heading', 'slug','author', 'body', 'status']