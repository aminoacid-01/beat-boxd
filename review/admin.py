from django.contrib import admin
from .models import Album, Review, Comment, Rating
from django_summernote.admin import SummernoteModelAdmin

class ReviewInline(admin.TabularInline):
    model = Review
    fields = ('author', 'heading', 'excerpt')
    readonly_fields = ('author', 'heading', 'excerpt',)
    extra = 0

class CommentInline(admin.TabularInline):
    model = Comment
    fields = ('author', 'body')
    readonly_fields = ('author', 'body')
    extra = 0

class RatingInline(admin.TabularInline):
    model = Rating
    fields = ('user', 'value')
    readonly_fields = ('author', 'value')
    extra = 0

class AlbumInline(admin.TabularInline):
    model = Album
    fields = ('title', 'artist')
    readonly_fields = ('title', 'artist')
    extra = 0

@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    list_display = ('heading', 'slug', 'status', 'created_on', 'updated_on', 'author')
    search_fields = ['heading', 'body']
    list_filter = ('status',)
    summernote_fields = ('body',)
    inlines = [
        CommentInline]

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('user', 'album', 'review', 'value')
    list_filter = ('value', 'album',)

# Register your models here.
@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('title', 'artist', 'release_date', 'average_rating', 'review_count')
    search_fields = ['title', 'artist']
    list_filter = ('artist',)
    inlines = [ReviewInline]

    def review_count(self, obj):
        return obj.review_set.count()
    review_count.short_description = 'Num of Reviews'

    def average_rating(self, obj):
        return obj.average_rating()
    average_rating.short_description = 'Average Rating'


@admin.register(Comment)
class CommentAdmin(SummernoteModelAdmin):
    list_display = ('author','body','created_on')
    search_fields = ['name', 'body']
    list_filter = ('created_on','approved')
    summernote_fields = ('body',)
