from django.urls import path
from .views import (
    Home,
    News_details,
    postComment,
    News_page,
    News_tag,
    Who_us,
    Search_news,
    Last_news,
    most_read,
    most_comment,
    create_category,
)

urlpatterns = [
    # Home page
    path('', Home, name='home'),
    # News details page
    path('news/<int:pk>', News_details, name='news_details'),
    # Add Comment by using AJAX
    path('post/ajax/comment/<int:pk>', postComment, name='post_comment'),
    # News page
    path('news-category/<int:pk>/<int:page>/', News_page, name='news_category'),
    # News tag
    path('news-tag/<int:pk>/<int:page>/', News_tag, name='news_tag'),
    # Who us
    path('who-us/', Who_us, name='who-us'),
    # Search page
    path('search-news/<int:page>', Search_news, name='search-news'),
    # Last News
    path('last-news/<int:page>/', Last_news, name='last-news'),
    # Most read
    path('most-read/<int:page>/', most_read, name='most-read'),
    # Most comment
    path('most-comment/<int:page>/', most_comment, name='most-comment'),
    # create category default settings
    path('default/', create_category, name='default'),

]
