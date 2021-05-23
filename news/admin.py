from django.contrib import admin
from .models import News, Comment, Category, Advertising, Photo, Note, Tag, Tag_news
# Register your models here.

admin.site.register(Category)
admin.site.register(News)
admin.site.register(Advertising)
admin.site.register(Comment)
admin.site.register(Photo)
admin.site.register(Note)
admin.site.register(Tag)
admin.site.register(Tag_news)

