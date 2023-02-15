from django.contrib import admin

from reviews.models import Category, Genre, Title, GenreTitle


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


class GenreAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'slug')
    search_fields = ('name',)
    list_filter = ('name',)


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


class GenreTitleAdmin(admin.ModelAdmin):
    list_display = ('genre', 'title')
    search_fields = ('title',)


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(GenreTitle, GenreTitleAdmin)
