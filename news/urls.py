from django.urls import path
from .views import (
    Home,
    News_details,
)

urlpatterns = [
    path('', Home, name='home'),
    path('news/<int:pk>', News_details, name='news_details'),
]
