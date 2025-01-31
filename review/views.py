from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from .models import Review

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
                  'review_list.html', 
                  {'reviews': reviews}
                  )
