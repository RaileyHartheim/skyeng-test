from django.contrib import admin

from .models import Review, UploadedFile

@admin.register(UploadedFile)
class FileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'file',
        'owner',
        'status',
        'upload_time')
    search_fields = ('owner', 'status,')
    list_filter = ('owner',)
    empty_value_display = '-пусто-'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'file',
        'owner',
        'status',
        'review_text',
        'review_errors',
        'check_time')
    search_fields = ('owner', 'status',)
    list_filter = ('owner',)
    empty_value_display = '-пусто-'
