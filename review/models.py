from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django.utils.text import slugify
import os
import requests
from datetime import datetime

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
        tracklist (list): A list of tracks on the album.
        release_date (date): The release date of the album.

    Methods:
        save: Save the album instance. Store artist names and album titles in lowercase.
        average_rating: Calculate the average rating of the album.
        __str__: Return a string representation of the album.
        
    """
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    image_url = models.URLField(blank=True, null=True)
    description = models.TextField(blank=True, null=True) 
    tracklist = models.JSONField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)

    def save(self, *args, **kwargs):
        # Store artist names and album titles in lowercase
        self.title = self.title.lower()
        self.artist = self.artist.lower()
        super().save(*args, **kwargs)

    def average_rating(self):
        ratings = self.ratings.all()
        if ratings.exists():
            return ratings.aggregate(models.Avg('value'))['value__avg']
        return 0

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
    rating = models.OneToOneField('Rating', on_delete=models.CASCADE, related_name='review_rating', blank=True, null=True)
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

        # Check if the album already exists
        existing_album = Album.objects.filter(title=self.album.title, artist=self.album.artist).first()
        if existing_album:
            self.album = existing_album

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
        try:
            response = requests.get(API_URL, params=params)
            response.raise_for_status()  # Raise an HTTPError for bad responses
            data = response.json()
            if 'album' in data:
                album_data = data['album']
                self.album.image_url = album_data['image'][-1]['#text']  # Get the largest image
                self.album.description = album_data.get('wiki', {}).get('summary', '')  # Get the album description
                tracks = album_data.get('tracks', {}).get('track', [])
                published_date = album_data.get('wiki', {}).get('published', 'N/A')
                if published_date != 'N/A':
                    try:
                        self.album.release_date = datetime.strptime(published_date, '%d %b %Y, %H:%M').date()
                    except ValueError:
                        self.album.release_date = None
                if isinstance(tracks, list):
                    self.album.tracklist = [track['name'] for track in tracks]
                elif isinstance(tracks, dict):
                    self.album.tracklist = [tracks['name']]
                else:
                    self.album.tracklist = []
                self.album.save()
                return album_data
        except requests.exceptions.RequestException as e:
            # Handle any request exceptions (e.g., network issues, invalid responses)
            print(f"Error fetching album info: {e}")
        except ValueError as e:
            # Handle JSON decoding errors
            print(f"Error decoding JSON response: {e}")
        return None

class Rating(models.Model):
    """
    Model representing a rating for an album.

    Attributes:
        album (Album): The album the rating belongs to.
        user (User): The user who rated the album.
        value (int): The value of the rating.

    Methods:
        __str__: Return a string representation of the rating.

        Class Meta:
            unique_together: Ensure that each user can only rate an album once.

    """
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name='ratings')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='review_rating', blank=True, null=True)
    value = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], blank=True)  # Limit value between 1 and 5

    class Meta:
        unique_together = ['album', 'user']

    def __str__(self):
        return f"{self.value}"
    
class Comment(models.Model):
    """
    Model representing a comment on a review.

    Attributes:
        review (Review): The review the comment belongs to.
        author (User): The author of the comment.
        body (str): The body of the comment.
        created_on (DateTime): The date and time the comment was created.
        updated_on (DateTime): The date and time the comment was last updated.
        approved (bool): Whether the comment is approved or not.
    """
    review = models.ForeignKey(Review, on_delete=models.CASCADE,related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    approved = models.BooleanField(default=False)