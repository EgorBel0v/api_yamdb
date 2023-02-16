from django.contrib import admin

from .models import User, Category, Genre, Title, GenreTitle


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    """Админ зона пользователей."""

    list_display = (
        'username',
        'email',
        'role',
        'bio',
        'first_name',
        'last_name',
    )
    list_editable = ('role',)
    list_filter = ('username', 'role',)
    search_fields = ('username', 'role',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = (
        'pk',
        'name',
        'year',
        'description',
        'get_genre',
        'category'
    )
    search_fields = ('name', 'year', 'category', 'genre')
    list_filter = ('name',)

    def get_genre(self, object):
        return '\n'.join((genre.name for genre in object.genre.all()))


@admin.register(GenreTitle)
class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('genre', 'title')
    search_fields = ('title',)
