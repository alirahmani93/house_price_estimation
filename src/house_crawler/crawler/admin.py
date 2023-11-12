from django.contrib import admin

from .models import Post, PostToken


class Admin(admin.ModelAdmin):
    list_filter = ['is_active', 'created_at']


class PostAdmin(Admin):
    list_display = ['token', 'city', 'title', 'price']


class PostTokenAdmin(Admin):
    list_display = ['code', 'is_active', ]


admin.site.register(Post, PostAdmin)
admin.site.register(PostToken, PostTokenAdmin)
