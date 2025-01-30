from django.urls import path
from .views import review_detail

urlpatterns = [
    path('review/<slug:slug>/', review_detail, name='review_detail'),
]