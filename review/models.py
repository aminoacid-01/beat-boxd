from django.db import models
from django.contrib.auth.models import User
import os
import requests


# Create your models here.

API_URL = 'http://ws.audioscrobbler.com/2.0/'

class Album(models.Model):
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    image_url = models.URLField(blank=True)

    def __str__(self):
        return f"{self.title} by {self.artist}"

class Review(models.Model):
    heading = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    excerpt = models.TextField(blank=True)

    def __str__(self):
        return self.heading

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
                self.name = data['album']['name']
                self.image_url = data['album']['image'][-1]['#text']  # Get the largest image
                self.save()
                return data['album']
        return None