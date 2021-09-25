from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    # ページ画面
    path('', views.index, name='top'),
    path('detail/<str:pk>/', views.detail, name='detail'),
    path('contact/', views.ContactView.as_view(), name='contact'),

    # 検索画面
    path('category_list/<str:slug_eng>', views.CategoryDetail.as_view(), name='categorylist'),
    path('tag_list/<str:tag_eng>', views.TagDetail.as_view(), name='taglist'),
    path('search/', views.Search, name='search'),
    
    # アカウント画面
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]

