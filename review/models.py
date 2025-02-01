from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
import os
import requests

# Create your models here.

API_URL = 'http://ws.audioscrobbler.com/2.0/'

class Album(models.Model):
    """
    Model representing an album.
    
    Attributes:
        title (str): The title of the album.
        artist (str): The name of the artist.
        image_url (str): The URL of the album cover image.
        description (str): A description of the album.

    Methods:
        save: Save the album instance. Store artist names and album titles in lowercase.
        __str__: Return a string representation of the album.
        
    """
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    image_url = models.URLField(blank=True)
    description = models.TextField(blank=True)  # Add a field for the description

    def save(self, *args, **kwargs):
        # Store artist names and album titles in lowercase
        self.title = self.title.lower()
        self.artist = self.artist.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Review(models.Model):
    """
    Model representing a review.

    Attributes:
        heading (str): The heading of the review. (originally meant to be title but kept on getting confused with album title)
        slug (str): The slug for the review.
        author (User): The author of the review.
        album (Album): The album being reviewed.
        body (str): The body of the review.
        created_on (DateTime): The date and time the review was created.
        updated_on (DateTime): The date and time the review was last updated.
        excerpt (str): An excerpt of the review.
        status (int): The status of the review (Draft or Published).

    Methods:
        save: Save the review instance. Automatically generate a slug if not provided.
        __str__: Return a string representation of the review.
        fetch_album_info: Fetch album information using the Last.fm API.
    """
    heading = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    excerpt = models.TextField(blank=True)
    STATUS = (
        (0, "Draft"),
        (1, "Published"),
    )
    status = models.IntegerField(choices=STATUS, default=0)

    def save(self, *args, **kwargs):
        # If the excerpt is empty, set it to the first 250 characters of the body
        if not self.excerpt:
            if len(self.body) > 250:
                self.excerpt = self.body[:247] + '...'
            else:
                self.excerpt = self.body

        # Automatically generate a slug if it's not provided
        if not self.slug:
            self.slug = slugify(self.heading)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.heading} by {self.author} | {self.album.title}"

    def fetch_album_info(self):
        # Fetch album info using the Last.fm API
        params = {
            'method': 'album.getinfo',
            'api_key': os.environ.get("LASTFM_API_KEY"),
            'artist': self.album.artist,
            'album': self.album.title,
            'format': 'json'
        }
        response = requests.get(API_URL, params=params)
        if response.status_code == 200:
            data = response.json()
            if 'album' in data:
                album_data = data['album']
                self.album.image_url = album_data['image'][-1]['#text']  # Get the largest image
                self.album.description = album_data.get('wiki', {}).get('summary', '')  # Get the album description
                self.album.save()
                return album_data
        return None