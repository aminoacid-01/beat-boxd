from django.urls import path
from . import views


urlpatterns = [
    path('', views.recent_review_list,
         name='home_page'),
    path('api/albums/<int:album_id>/', views.album_detail,
         name='album_detail'),
    path('create/', views.create_review,
         name='create_review'),
    path('reviews/', views.review_list,
         name='review_list'),
    path('reviews/user', views.user_review_list,
         name='user_reviews'),
    path('reviews/<slug:slug>/', views.review_detail,
         name='review_detail'),
    path('reviews/<slug:slug>/delete/', views.delete_review,
         name='delete_review'),
    path('reviews/<slug:slug>/edit/', views.edit_review,
         name='edit_review'),
]
