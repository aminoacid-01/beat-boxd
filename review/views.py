from django.http import JsonResponse
from django.shortcuts import get_object_or_404,render
from .models import Review

def review_detail(request, slug):
    review = get_object_or_404(Review, slug=slug)
    album_info = review.fetch_album_info()
    if album_info:
        return JsonResponse({'status': 'success', 'album_info': album_info})
    else:
        return JsonResponse({'status': 'failure', 'message': 'Album information could not be fetched'})
    
def review_list(request):
    reviews = Review.objects.all()
    for review in reviews:
        review.fetch_album_info()  # Fetch album info for each review
    return render(request, 'review_list.html', {'reviews': reviews})