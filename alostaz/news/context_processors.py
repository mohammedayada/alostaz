from .models import Category
from user.models import Photo


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
