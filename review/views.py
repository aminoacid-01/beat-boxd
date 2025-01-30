from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from .models import Review

def review_detail(request, slug):
    review = get_object_or_404(Review, slug=slug)
    album_info = review.fetch_album_info()
    if album_info:
        return JsonResponse({'status': 'success', 'album_info': album_info})
    else:
        return JsonResponse({'status': 'failure', 'message': 'Album information could not be fetched'})