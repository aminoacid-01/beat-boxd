from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Review, Album, Comment
from .forms import AlbumForm, ReviewForm, CommentForm, RatingForm
from django.contrib.auth.decorators import login_required


# Review CRUD operations
def review_detail(request, slug):
    """
    Display an individual :model:`review.Review`.

    **Context**

    ``review``
        An instance of :model:`review.Review`.

    **Template:**

    :template:`review/review_detail.html`

    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the review to display.
    Returns:
        HttpResponse: The rendered 'review_detail.html' template with the review.
    """

    review = get_object_or_404(Review, slug=slug)
    comments = review.comments.filter(approved=True).order_by("-created_on")
    comment_count = comments.count()
    form_submitted = False
     # Fetch related reviews based on the same artist
    related_reviews = Review.objects.filter(album__artist=review.album.artist).exclude(id=review.id)[:5]

    #Comment Form
    if request.method == 'POST':
        if request.user.is_authenticated:
            if 'delete_comment_id' in request.POST:
                # Deleting an existing comment
                comment = get_object_or_404(Comment, id=request.POST.get('delete_comment_id'), author=request.user)
                comment.delete()
                form_submitted = False
                return redirect('review_detail', slug=review.slug)
            elif 'comment_id' in request.POST:
                # Editing an existing comment
                comment = get_object_or_404(Comment, id=request.POST.get('comment_id'), author=request.user)
                comment_form = CommentForm(request.POST, instance=comment)
                if comment_form.is_valid():
                    comment_form.save()
                    form_submitted = False
                    return redirect('review_detail', slug=review.slug)
            else:
                # Adding a new comment
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    new_comment = comment_form.save(commit=False)
                    new_comment.review = review
                    new_comment.author = request.user
                    new_comment.save()
                    form_submitted = True
                    return redirect('review_detail', slug=review.slug)
        else:
            return redirect('login')

    comment_form = CommentForm()

    # Fetch album information
    album_info = review.fetch_album_info()

    return render(
        request,
        "review_detail.html",
            {"review": review,
             "comments": comments,
             "comment_count": comment_count,
             "comment_form": comment_form,
             "form_submitted": form_submitted,
             "related_reviews": related_reviews,
             }
        )

def review_list(request):
    """
    View function to display a list of reviews.
    This function retrieves all reviews from the database, fetches additional
    album information for each review, and renders the 'review_list.html' template
    with the list of reviews.

    **Context**
    
    ``reviews``
        A queryset of all :model:`review.Review` instances.
    
    **Template:**
    
    :template:`review/review_list.html`

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered 'review_list.html' template with the list of reviews.
    """

    reviews = Review.objects.all().order_by('-created_on')
    for review in reviews:
        review.fetch_album_info()  # Fetch album info for each review
    return render(request, 
                  'review_list.html', 
                  {'reviews': reviews}
                  )


def recent_review_list(request):
    """
    View function to display a list of reviews.
    This function retrieves all reviews from the database, fetches additional
    album information for each review, and renders the 'review_list.html' template
    with the list of reviews.

    **Context**
    
    ``reviews``
        A queryset of all :model:`review.Review` instances.
    
    **Template:**
    
    :template:`review/review_list.html`

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered 'review_list.html' template with the list of reviews.
    """

    reviews = Review.objects.all().order_by('-created_on')[:6]  
    for review in reviews:
        review.fetch_album_info()  # Fetch album info for each review
    return render(request, 
                  'index.html', 
                  {'reviews': reviews}
                  )




@login_required
def create_review(request):
    """
    View function to create a new review.
    This function handles both GET and POST requests. For GET requests, it renders the 'create_review.html' template with empty forms. For POST requests, it processes the form data, creates a new album and review instance, and redirects the user to the home page. If the album already exists, the existing album instance is used.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered 'create_review.html' template with the album and review forms.
    """

    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        album_form = AlbumForm(request.POST)
        review_form = ReviewForm(request.POST)
        if album_form.is_valid() and review_form.is_valid and rating_form.is_valid():
            if album_form.cleaned_data['existing_album']:
                album = album_form.cleaned_data['existing_album']
            else:
                album = album_form.save(commit=False)
                album.title = album_form.cleaned_data['title']
                album.artist = album_form.cleaned_data['artist']
                album.image_url = album_form.cleaned_data['image_url']
                album.description = album_form.cleaned_data['description']
                album.save()
            review = review_form.save(commit=False)
            review.album = album
            review.author = request.user  # Set the author to the logged-in user
            review.save() # Save the review

            rating = rating_form.save(commit=False)
            rating.review = review
            rating.user = request.user
            rating.album = album
            rating.save()  # Save the rating

            review.rating = rating
            review.save()  # Save the review

            return redirect('home_page')
    else:
        album_form = AlbumForm()
        review_form = ReviewForm()
        rating_form = RatingForm()
    return render(request, 'create_review.html', {'album_form': album_form, 'review_form': review_form, 'rating_form': rating_form})

@login_required
def edit_review(request, slug):
    review = get_object_or_404(Review, slug=slug, author=request.user)
    if request.method == 'POST':
        form = ReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_detail', slug=review.slug)
    else:
        form = ReviewForm(instance=review)
    return render(request, 'edit_review.html', {'review_form': form, 'review': review})

@login_required
def delete_review(request, slug):
    review = get_object_or_404(Review, slug=slug, author=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('home_page')
    return render(request, 'delete_review.html', {'review': review})



def get_album_artist(request):
    """
    View function to get the artist of an album.
    This function takes a 'title' parameter from the query string and returns the artist of the album with that title. If the album does not exist, an empty string is returned. The artist is returned as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        JsonResponse: The artist of the album as a JSON response.
    """
    title = request.GET.get('title', None)
    if title:
        try:
            album = Album.objects.get(title__iexact=title.lower())
            return JsonResponse({'artist': album.artist})
        except Album.DoesNotExist:
            return JsonResponse({'artist': ''})
    return JsonResponse({'artist': ''})

def album_detail(request, album_id):
    album = Album.objects.get(id=album_id)
    data = {
        'title': album.title,
        'artist': album.artist,
        'image_url': album.image_url,
        'description': album.description,
    }
    return JsonResponse(data)
