from django.contrib import admin
from main.models import Perfil, Tweet


class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'name', 'image', 'birth_date', 'city', 'public', 'biography',)


class TweetAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'created_at',)

admin.site.register(Perfil, PerfilAdmin)
admin.site.register(Tweet, TweetAdmin)
