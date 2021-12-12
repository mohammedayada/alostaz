from django.contrib import admin
from .models import News, Comment, Category, Note, Tag, Tag_news, Book, Carton, Video, Audio, TV

# Register your models here.

admin.site.register(Category)
admin.site.register(News)
admin.site.register(Comment)
admin.site.register(Note)
admin.site.register(Tag)
admin.site.register(Tag_news)
admin.site.register(Book)
admin.site.register(Carton)
admin.site.register(Video)
admin.site.register(Audio)
admin.site.register(TV)