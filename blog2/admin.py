from django.contrib import admin
from .models import Blog, Category, Tags
from markdownx.admin import MarkdownxModelAdmin
# Register your models here.

admin.site.register(Blog, MarkdownxModelAdmin)
admin.site.register(Category)
admin.site.register(Tags)