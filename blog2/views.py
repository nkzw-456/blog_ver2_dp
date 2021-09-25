from typing import List
from django.shortcuts import render, redirect
from django.views.generic import ListView, TemplateView, DeleteView, FormView
from .models import Blog, Category, Comment, Tags
from django.core.paginator import Paginator
from .forms import CommentForm, SearchForm, ContactForm, LoginForm, UserCreationForm
from django.db.models import Q
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.views import LoginView, LogoutView


# Create your views here.

# class IndexView(ListView):
#     model = Blog
#     template_name = 'blog2/index.html'

def index(request):
    obj = Blog.objects.order_by('-created_at')
    object_list = Paginator(obj, 10)
    page_number = request.GET.get('page')
    category_list = Category.objects.all()
    tags_list = Tags.objects.all()
    context = {
        'object_list': object_list.get_page(page_number),
        'category_list': category_list,
        'tags_list': tags_list,
    }

    return render(request, 'blog2/index.html', context)


def detail(request, pk):
    obj = Blog.objects.get(pk=pk)
    comments = Comment.objects.filter(blog=obj)
    context = {
        'blog': obj,
        'comments': comments,
    }
    if request.method == 'POST':
        if request.POST.get('like_count', None):
            obj.count += 1
            obj.save()

        form = CommentForm(request.POST)
        if form.is_valid():
            text = form.save(commit=False)
            text.blog = obj
            text.save()
        
    return render(request, 'blog2/detail.html', context)


def Search(request):
    if request.method == 'POST':
        searchform = SearchForm(request.POST)

        if searchform.is_valid():
            freeword = searchform.cleaned_data['freeword']
            search_list = Blog.objects.filter(Q(title__icontains = freeword)|Q(text__icontains = freeword))

            context = {
                'search_list': search_list,
            }

            return render(request, 'blog2/search.html', context)


class CategoryDetail(ListView):
    model = Category
    slug_field = 'slug_eng'
    slug_url_kwarg = 'slug_eng'
    template_name = 'blog2/category_list.html'

    def get_context_data(self, *args, **kwargs):
        detail_data = Category.objects.get(slug_eng = self.kwargs['slug_eng'])
        category_posts = Blog.objects.filter(category = detail_data.id).order_by('-created_at')

        context = {
            'object': detail_data,
            'category_list': category_posts
        }

        return context


class TagDetail(ListView):
    model = Tags
    slug_field = 'tag_eng'
    slug_url_kwarg = 'tag_eng'
    template_name = 'blog2/tag_list.html'

    def get_context_data(self, *args, **kwargs):
        detail_data = Tags.objects.get(tag_eng = self.kwargs['tag_eng'])
        tag_posts = Blog.objects.filter(tag = detail_data.id).order_by('-created_at')

        context = {
            'object': detail_data,
            'tag_list': tag_posts,
        }

        return context


class ContactView(FormView):
    template_name = 'blog2/contact.html'
    form_class = ContactForm
    success_url = reverse_lazy("contact")

    def form_valid(self, form):
        form.send_email()
        return super().form_valid(form)


class Login(LoginView):
    form_class = LoginForm
    template_name = 'registration/login.html'
    
    def form_valid(self, form):
        messages.success(self.request, 'ログイン完了 ようこそ')
        return super().form_valid(form)


class Logout(LogoutView):
    template_name = 'registration/logout.html'


def signup(request):
    context = {}
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            messages.success(request, '登録完了!')
            return redirect('login')
    return render(request, 'registration/signup.html', context)
