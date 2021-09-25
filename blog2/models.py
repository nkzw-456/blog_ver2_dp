from django.db import models
from django.db.models.deletion import PROTECT
from django.db.models.fields import CharField
from markdownx.models import MarkdownxField
from django.utils.crypto import get_random_string


# Create your models here.
def create_id():
    return get_random_string(22)


class Category(models.Model):
    slug_name = models.CharField(max_length=20)
    slug_eng = models.CharField(max_length=20)

    def __str__(self):
        return self.slug_name

    def category_count(self):
        num = Blog.objects.filter(category = self).count()
        return num


class Tags(models.Model):
    tag_name = models.CharField(max_length=20)
    tag_eng = models.CharField(max_length=20)

    def __str__(self):
        return self.tag_name

    def tag_count(self):
        num = Blog.objects.filter(tag = self).count()
        return num


class Blog(models.Model):
    id = models.CharField(default=create_id, primary_key=True, max_length=22,
    editable=False)
    category = models.ForeignKey('Category', on_delete=PROTECT)
    tag = models.ManyToManyField('Tags', blank=True)
    title = models.CharField(max_length=30)
    text = MarkdownxField()
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.title

    def blog_count(self):
        num = Blog.objects.all().count()
        return num


class Comment(models.Model):
    text = models.TextField(max_length=1000, default='')
    name = models.CharField(max_length=20, default='')
    created_at = models.DateField(auto_now_add=True)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE)

    def __str__(self):
        return self.text[:10]