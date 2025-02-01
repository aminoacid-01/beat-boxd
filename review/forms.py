from django import forms
from .models import Album, Review
from django_summernote.widgets import SummernoteWidget


class AlbumForm(forms.ModelForm):
    existing_album = forms.ModelChoiceField(queryset=Album.objects.all(), required=False, empty_label="Select an existing album")

    class Meta:
        model = Album
        fields = ['existing_album','title', 'artist']

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