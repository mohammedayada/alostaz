from django.urls import path
from .views import (
    Home,
    News_details,
    postComment,
    News_page,
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

]
