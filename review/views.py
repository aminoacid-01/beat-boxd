from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Review, Album
from .forms import AlbumForm, ReviewForm
from django.contrib.auth.decorators import login_required

def review_detail(request, slug):
    """
    Display an individual :model:`review.Review`.

    **Context**

    ``review``
        An instance of :model:`review.Review`.

    **Template:**

    :template:`review/review_detail.html`
    """

    review = get_object_or_404(Review, slug=slug)

    # Fetch album information
    album_info = review.fetch_album_info()

    return render(
        request,
        "review_detail.html",
        {"review": review},
    )

def review_list(request):
    """
    View function to display a list of reviews.
    This function retrieves all reviews from the database, fetches additional
    album information for each review, and renders the 'review_list.html' template
    with the list of reviews.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered 'review_list.html' template with the list of reviews.
    """

    reviews = Review.objects.all().order_by('-created_on')  # Get all reviews from the database
    for review in reviews:
        review.fetch_album_info()  # Fetch album info for each review
    return render(request, 
                  'index.html', 
                  {'reviews': reviews}
                  )


@login_required
def create_review(request):
    if request.method == 'POST':
        album_form = AlbumForm(request.POST)
        review_form = ReviewForm(request.POST)
        if album_form.is_valid() and review_form.is_valid():
            album = album_form.save()
            review = review_form.save(commit=False)
            review.album = album
            review.author = request.user  # Set the author to the logged-in user
            review.save()
            return redirect('review_list')
    else:
        album_form = AlbumForm()
        review_form = ReviewForm()
    return render(request, 'create_review.html', {'album_form': album_form, 'review_form': review_form})
