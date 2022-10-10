from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title, User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'username',
        'first_name',
        'last_name',
        'email',
        'role',
        'bio',
        'confirmation_code',
    )
    search_fields = ('username', 'role',)
    list_filter = ('username', 'role',)
    empty_value_display = '-пусто-'


@admin.register(Category, Genre, Title, Review, Comment)
class BaseAdmin(admin.ModelAdmin):
    empty_value_display = '-пусто-'
