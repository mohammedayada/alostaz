from django.urls import path
from .views import (
    Home,
    News_details,
    postComment,
)

urlpatterns = [
    path('', Home, name='home'),
    path('news/<int:pk>', News_details, name='news_details'),
    path('post/ajax/comment/<int:pk>', postComment, name='post_comment'),
]
