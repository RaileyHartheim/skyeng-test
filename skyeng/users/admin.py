from django.contrib import admin

from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email',)
    search_fields = ('email',)
    list_filter = ('email',)
    empty_value_display = '-пусто-'
