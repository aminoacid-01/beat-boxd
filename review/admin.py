from django.contrib import admin
from .models import Album, Review
from django_summernote.admin import SummernoteModelAdmin

@admin.register(Review)
class ReviewAdmin(SummernoteModelAdmin):
    list_display = ('heading', 'slug', 'status')
    search_fields = ['heading', 'body']
    list_filter = ('status',)
    summernote_fields = ('body',)

# Register your models here.
admin.site.register(Album)