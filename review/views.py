from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render, redirect
from .models import Review, Album, Comment, Rating
from .forms import AlbumForm, ReviewForm, CommentForm, RatingForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages


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
        else:
            return redirect('account_login')

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

    reviews = Review.objects.filter(status =1).order_by('-created_on')
    paginator = Paginator(reviews, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    for review in page_obj:
        review.fetch_album_info()  # Fetch album info for each review
    return render(request, 
                  'review_list.html', 
                  {'reviews': page_obj,
                   'page_obj': page_obj}
                  )

@login_required
def user_review_list(request):
    '''
    A view function to display a list of reviews by the user that is currently logged in.

    Args:
        request (HttpRequest): The HTTP request object.
    
    Returns:
        HttpResponse: The rendered 'user_review_list.html' template with the list of reviews.
    '''
    reviews = Review.objects.filter(author=request.user, status=1).order_by('-created_on')
    paginator = Paginator(reviews, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    for review in page_obj:
        review.fetch_album_info()  # Fetch album info for each review
    return render(request, 
                  'user_review_list.html', 
                  {'reviews': page_obj,
                   'page_obj': page_obj}
                  )


def recent_review_list(request):
    """
    This function retrieves the most recent reviews from the database, fetches additional
    album information for each review, and renders the 'index.html' template with the list of reviews.

    **Context**
    
    ``reviews``
        A queryset of the most recent :model:`review.Review` instances.
    
    **Template:**
    
    :template:`index.html`

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered 'index.html' template with the list of recent reviews.
    """

    reviews = Review.objects.filter(status=1).order_by('-created_on')[:6]  
    for review in reviews:
        review.fetch_album_info()  # Fetch album info for each review
    return render(request, 
                  'index.html', 
                  {'reviews': reviews}
                  )




@login_required
def create_review(request):
    """
    Handles the creation of a new review and rating for an album.

    Args:
        request (HttpRequest): The HTTP request object.
    Returns:
        HttpResponse: The rendered 'create_review.html' template with the album and review forms.
    """
    if request.method == 'POST':
        rating_form = RatingForm(request.POST)
        album_form = AlbumForm(request.POST)
        review_form = ReviewForm(request.POST)

        if album_form.is_valid() and review_form.is_valid() and rating_form.is_valid():
            review = review_form.save(commit=False)
            if album_form.cleaned_data['existing_album']:
                album = album_form.cleaned_data['existing_album']
            else:
                album = album_form.save(commit=False)
                album.title = album_form.cleaned_data['title']
                album.artist = album_form.cleaned_data['artist']
                album.image_url = album_form.cleaned_data['image_url']
                album.description = album_form.cleaned_data['description']
                album.save()

            review.album = album
            review.author = request.user  # Set the author to the logged-in user
            review.status = 1

            # Check if a rating by the same user for the same album already exists
            if Rating.objects.filter(album=album, user=request.user).exists():
                rating_form.add_error('value', "You have already rated this album.")
            else:
                review.save()  # Save the review
                rating = rating_form.save(commit=False)
                rating.review = review
                rating.user = request.user
                rating.album = album
                rating.save()  # Save the rating

                review.rating = rating
                review.save()  # Save the review

                messages.success(request, 'Review and rating submitted successfully!')
                return redirect('home_page')
    else:
        album_form = AlbumForm()
        review_form = ReviewForm()
        rating_form = RatingForm()

    return render(request, 'create_review.html', {
        'album_form': album_form,
        'review_form': review_form,
        'rating_form': rating_form,
    })

@login_required
def edit_review(request, slug):
    """
    Handle the editing of a review.
    This view allows the author of a review to edit their review. If the request method is POST,
    it will attempt to update the review with the provided data. If the form is valid, the review
    is saved and the user is redirected to the review detail page. If the request method is GET,
    it will display the form with the current review data.
    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the review to be edited.
    Returns:
        HttpResponse: The response object containing the rendered template.
    """
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
    '''
    This function deletes a review.
    Args:
        request (HttpRequest): The HTTP request object.
        slug (str): The slug of the review to delete.
        
    Returns:
        HttpResponse: The rendered 'delete_review.html' template with the review.
        '''
    review = get_object_or_404(Review, slug=slug, author=request.user)
    if request.method == 'POST':
        review.delete()
        return redirect('home_page')
    return render(request, 'delete_review.html', {'review': review})



def album_detail(request, album_id):
    """
    Retrieve and return the details of a specific album as a JSON response.
    Args:
        request (HttpRequest): The HTTP request object.
        album_id (int): The ID of the album to retrieve.
    Returns:
        JsonResponse: A JSON response containing the album details, including
                      title, artist, image_url, and description.
    """

    album = Album.objects.get(id=album_id)
    data = {
        'title': album.title,
        'artist': album.artist,
        'image_url': album.image_url,
        'description': album.description,
    }
    return JsonResponse(data)
