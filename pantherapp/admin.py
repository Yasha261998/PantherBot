from django.contrib import admin
from .models import CustomUser


@admin.register(CustomUser)
class ItemsAdmin(admin.ModelAdmin):
    list_display = ('id_telegram', 'username', 'first_name')
    list_display_links = ['username']
