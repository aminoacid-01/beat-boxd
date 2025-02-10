from django.test import TestCase
from .forms import CommentForm, ReviewForm, AlbumForm, RatingForm

# Create your tests here.


class TestCommentForm(TestCase):
    def test_form_is_valid(self):
        comment_form = CommentForm({
            'body': 
            'This is a great post'
            })
        self.assertTrue(comment_form.is_valid())


    def test_form_is_invalid(self):
        comment_form = CommentForm({'body': ''})
        self.assertFalse(
            comment_form.is_valid(),
            msg="Form is valid"
            )


class TestReviewForm(TestCase):
    def test_form_is_valid(self):
        review_form = ReviewForm({
            'heading': 'This is a great post',
            'body': 'This is a great post',
            })
        self.assertTrue(review_form.is_valid())


    def test_form_is_invalid(self):
        review_form = ReviewForm({
            'heading': '',
            'body' : ''})
        self.assertFalse(
            review_form.is_valid(), 
            msg="Form is valid"
            )

    def test_form_is_invalid_empty_heading(self):
        review_form = ReviewForm({
            'heading': '',
            'body': 'This is a great post'
        })
        self.assertFalse(
            review_form.is_valid(), 
            msg="Form is valid"
            )

    def test_form_is_invalid_empty_body(self):
        review_form = ReviewForm({
            'heading': 'This is a great post',
            'body': ''
        })
        self.assertFalse(
            review_form.is_valid(), 
            msg="Form is valid"
            )


class TestAlbumForm(TestCase):
    def test_form_is_valid(self):
        album_form = AlbumForm({
            'title': 'Infinity On A High',
            'artist': 'Fall Out Boy',
            'image_url': 'http://example.com/image.jpg',
            'description': 'A great album by Fall Out Boy'
        })
        self.assertTrue(album_form.is_valid())


class TestRatingForm(TestCase):
    def test_form_is_valid(self):
        rating_form = RatingForm({'value': 3})
        self.assertTrue(rating_form.is_valid())

    def test_form_is_invalid_too_low(self):
        rating_form = RatingForm({'value': 0})
        self.assertFalse(rating_form.is_valid(), msg="Form is valid")

    def test_form_is_invalid_too_high(self):
        rating_form = RatingForm({'value': 6})
        self.assertFalse(rating_form.is_valid(), msg="Form is valid")