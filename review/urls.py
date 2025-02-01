from django.urls import path
from . import views


urlpatterns = [
    path('', views.review_list, name='home_page'),
    path('api/albums/<int:album_id>/', views.album_detail, name='album_detail'),
    path('reviews/<slug:slug>/', views.review_detail, name='review_detail'),
    path('create/', views.create_review, name='create_review'),
]