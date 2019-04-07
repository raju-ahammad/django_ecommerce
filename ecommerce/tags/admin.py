from django.contrib import admin

# Register your models here.
from .models import Tag


class TagAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug',)
admin.site.register(Tag, TagAdmin)
