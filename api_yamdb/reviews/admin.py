from django.contrib import admin
from .models import User

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
