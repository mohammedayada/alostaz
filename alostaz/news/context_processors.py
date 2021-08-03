from .models import News, Category, Note, Comment, Tag_news, Tag, Book, Carton, Video, Audio, TV
from user.models import user, Photo, Advertising, Survey

def categories_processor(request):
    categories = Category.objects.filter(parent=None)
    photo1 = Photo.objects.filter(pk=1).last()
    photo2 = Photo.objects.filter(pk=2).last()
    photo3 = Photo.objects.filter(pk=3).last()
    return {'categories': categories,
            'photo1': photo1,
            'photo2': photo2,
            'photo3': photo3,
            }
