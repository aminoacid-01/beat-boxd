from django import forms
from .models import Album, Review

class AlbumForm(forms.ModelForm):
    class Meta:
        model = Album
        fields = ['title', 'artist']

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['heading', 'body', 'status']