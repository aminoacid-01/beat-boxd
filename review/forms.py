from django import forms
from .models import Album, Review, Comment
from django_summernote.widgets import SummernoteWidget

class AlbumForm(forms.ModelForm):
    existing_album = forms.ModelChoiceField(queryset=Album.objects.all(), required=False, empty_label="Select an existing album")

    class Meta:
        model = Album
        fields = ['existing_album', 'title', 'artist', 'image_url', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['artist'].required = False
        self.fields['image_url'].required = False
        self.fields['description'].required = False

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['heading', 'body', 'status']
        widgets = {
            'body': SummernoteWidget(),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        widgets = {
            'body': SummernoteWidget(),
        }
        labels = {
            'body': 'Type Your Comment Here',
        }