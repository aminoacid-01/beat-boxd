from django import forms
from .models import Album, Review, Comment, Rating
from django_summernote.widgets import SummernoteWidget


class AlbumForm(forms.ModelForm):
    existing_album = forms.ModelChoiceField(
        queryset=Album.objects.all(),
        required=False,
        empty_label="Select an existing album"
    )

    class Meta:
        model = Album
        fields = [
            'existing_album',
            'title',
            'artist',
            'image_url',
            'description'
        ]
        labels = {
            'title': 'Album Title',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['title'].required = False
        self.fields['artist'].required = False
        self.fields['image_url'].required = False
        self.fields['description'].required = False


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['heading', 'body']
        labels = {
            'heading': 'Title',
            'body': 'Review',
        }
        widgets = {
            'body': SummernoteWidget(),
        }


class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['value']
        labels = {
            'value': 'Rating',
        }
        widgets = {
            'value': forms.NumberInput(attrs={'min': 1, 'max': 5}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].required = True


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['body']
        labels = {
            'body': 'Type Your Comment Here',
        }
        widgets = {
            'body': forms.Textarea,
        }
