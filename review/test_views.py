from django.test import TestCase, Client
from django.urls import reverse
from .models import Review, Album, Comment, Rating, Album
from .forms import CommentForm, ReviewForm, AlbumForm, RatingForm
from django.contrib.auth.models import User


class ReviewViewsTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser',
                                             password='12345')
        self.album = Album.objects.create(
            title='testalbum',
            artist='testartist',
            image_url='static/images/placeholder_cover.jpg',
            description='test description',
            tracklist=['test track']
        )
        self.review = Review.objects.create(
            heading='test review',
            author=self.user,
            album=self.album,
            body='test body',
            status=1
        )
        self.comment = Comment.objects.create(
            author=self.user,
            review=self.review,
            body='test comment',
            approved=True
        )
        self.rating = Rating.objects.create(
            user=self.user,
            album=self.album,
            value=5
        )

    def test_review_detail_view(self):
        response = self.client.get(reverse('review_detail',
                                           args=[self.review.slug]))
        print(f"Debug: Response content - {response.content.decode('utf-8')}")
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_detail.html')
        self.assertContains(response, self.review.heading)
        self.assertContains(response, self.review.body)
        self.assertContains(response, self.review.author.username)
        self.assertContains(response, self.comment.body)
        self.assertIsInstance(
            response.context['comment_form'], CommentForm)

    def test_review_list_view(self):
        response = self.client.get(reverse('review_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'review_list.html')
        self.assertContains(response, self.review.heading)

    def test_user_review_list_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('user_reviews'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'user_review_list.html')
        self.assertContains(response, self.review.heading)

    def test_recent_review_list_view(self):
        response = self.client.get(reverse('home_page'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'index.html')
        self.assertContains(response, self.review.heading)

    def test_create_review_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('create_review'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_review.html')
        self.assertIsInstance(
            response.context['review_form'], ReviewForm)
        self.assertIsInstance(
            response.context['rating_form'], RatingForm)
        self.assertIsInstance(
            response.context['album_form'], AlbumForm)

    def test_edit_review_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('edit_review',
                                           args=[self.review.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_review.html')
        self.assertIsInstance(
            response.context['review_form'], ReviewForm)

    def test_delete_review_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.get(reverse('delete_review',
                                           args=[self.review.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'delete_review.html')

    def test_album_detail_view(self):
        response = self.client.get(reverse('album_detail',
                                           args=[self.album.id]))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {
            'title': self.album.title,
            'artist': self.album.artist,
            'image_url': self.album.image_url,
            'description': self.album.description,
        })
