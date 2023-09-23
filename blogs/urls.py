from django.urls import path
from . import views

urlpatterns = [
    path('blogs/', views.BlogView.as_view(),name='blog'),
    path('blog/<int:pk>/', views.BlogViewDetail.as_view(),name='blogdetail'),
    path('comment/<int:pk>/', views.CommentViewDetail.as_view(),name='commentdetail'),
    path('blog/search/', views.SearchView.as_view(),name='search'),
]