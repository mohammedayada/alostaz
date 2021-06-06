from django.shortcuts import render, redirect
from .models import News, Category, Note, Comment, Tag_news, Tag
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from user.models import user, Photo, Advertising

# Create your views here.
# Make a regular expression
# for validating an Email
regex = '^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'


# Define a function for
# for validating an Email
def check(email):
    # pass the regular expression
    # and the string in search() method
    if re.search(regex, email):
        return True
    else:
        return False


# Home functions
def Home(request):
    # Latest news أحدث الأخبار
    latest_news = News.objects.filter(approval=True).order_by('-Publish_date')[:5]
    # Breaking news أخبار عاجله
    breaking_news0 = News.objects.filter(approval=True).order_by('-Publish_date')[:8]
    breaking_news1 = News.objects.filter(approval=True).order_by('-Publish_date')[8:16]
    # Local news المحليات
    local = Category.objects.filter(name='محليات').last()
    local_news = News.objects.filter(category=local, approval=True).order_by('-Publish_date')[:9]
    # Arabs and the world عرب وعالم
    arab_and_world = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='عرب وعالم') | Q(category__name='عرب وعالم'))).order_by(
        '-Publish_date')[:9]
    # حوادث وتحقيقات Accidents and investigations
    accidents_and_investigations = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='حوادث وتحقيقات') | Q(category__name='حوادث وتحقيقات'))).order_by(
        '-Publish_date')[:9]
    # Politics and Economy سياسه واقتصاد
    politics_and_economy = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='سياسه وأقتصاد') | Q(category__name='سياسه وأقتصاد'))).order_by(
        '-Publish_date')[:9]
    # sport رياضة
    sports = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='رياضة') | Q(category__name='رياضة'))).order_by('-Publish_date')[
             :9]
    # Culture and arts ثقافه وفنون
    culture_and_arts = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='ثقافة وفنون') | Q(category__name='ثقافة وفنون'))).order_by(
        '-Publish_date')[:9]
    # Talents and identities مواهب وهوايات
    talents_and_identities = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='مواهب وهويات') | Q(category__name='مواهب وهويات'))).order_by(
        '-Publish_date')[:9]
    # Real Estate and Cars عقارات وسيارات
    real_estate_and_cars = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='عقارات وسيارات') | Q(category__name='عقارات وسيارات'))).order_by(
        '-Publish_date')[:9]
    # Video and audio صوت وصوره
    video_and_audio = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='صوت وصورة') | Q(category__name='صوت وصورة'))).order_by(
        '-Publish_date')[:9]
    # ناس ومجتمع
    people_and_society = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='ناس ومجتمع') | Q(category__name='ناس ومجتمع'))).order_by(
        '-Publish_date')[:9]
    # منوعات
    mixs = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='حوادث وتحقيقات') | Q(category__name='حوادث وتحقيقات'))).order_by(
        '-Publish_date')[:9]
    # محافظات cites
    cites = News.objects.filter(
        Q(approval=True) & (Q(category__parent__name='محافظات') | Q(category__name='محافظات'))).order_by(
        '-Publish_date')[:9]
    # محافظات cites
    books1 = News.objects.filter(
        Q(approval=True) & Q(category__name='كتب')).order_by(
        '-Publish_date')[:5]
    books2 = News.objects.filter(
        Q(approval=True) & Q(category__name='كتب')).order_by(
        '-Publish_date')[5:10]
    # Most read الأكثر قراءه
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
    # Notes العناوين
    notes = Note.objects.all().order_by('-id')
    # Notes العناوين
    photo1 = Photo.objects.filter(pk=1).last()
    photo2 = Photo.objects.filter(pk=2).last()
    photo3 = Photo.objects.filter(pk=3).last()
    photo4 = Photo.objects.filter(pk=4).last()
    photo5 = Photo.objects.filter(pk=5).last()
    photos = Photo.objects.all()[5:]
    advertisings = Advertising.objects.all()
    cartons = News.objects.filter(pk=65)[:4]
    more_comments = News.objects.all().order_by('commentCount')[:6]
    context = {
        'latest_news': latest_news,
        'local_news': local_news,
        'arab_and_world': arab_and_world,
        'accidents_and_investigations': accidents_and_investigations,
        'politics_and_economy': politics_and_economy,
        'sports': sports,
        'culture_and_arts': culture_and_arts,
        'talents_and_identities': talents_and_identities,
        'real_estate_and_cars': real_estate_and_cars,
        'video_and_audio': video_and_audio,
        'people_and_society': people_and_society,
        'mixs': mixs,
        'cites': cites,
        'books1': books1,
        'books2': books2,
        'breaking_news0': breaking_news0,
        'breaking_news1': breaking_news1,
        'most_read': most_read,
        'notes': notes,
        'photo1': photo1,
        'photo2': photo2,
        'photo3': photo3,
        'photo4': photo4,
        'photo5': photo5,
        'photos': photos,
        'advertisings': advertisings,
        'cartons': cartons,
        'more_comments': more_comments,

    }
    return render(request, 'index.html', context)


# News details page
def News_details(request, pk):
    news = News.objects.filter(pk=pk).last()
    username = 'غير معروف'
    name = user.objects.filter(id=news.user.id).last()
    if name:
        username = name.name
    if news.approval == False:
        if request.user.is_authenticated:
            my_user = user.objects.get(id=request.user.id)
            if my_user.type == 'chairman' or my_user.type == 'editor_in_chief' or news.user == my_user:
                pass
        else:
            return redirect('home')

    # To increament news count
    news.incrementViewCount()
    # Most read الأكثر قراءه
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
    # comments for this post
    comments = Comment.objects.filter(news=news, approval=True)
    # Tags
    tag_news = Tag_news.objects.filter(news=news)
    # Related News الموضوعات المتعلقه
    related_news = News.objects.filter(Q(approval=True) & Q(category=news.category) & ~Q(pk=news.pk)).order_by(
        '-Publish_date')[:3]
    photo1 = Photo.objects.filter(pk=1).last()
    photo2 = Photo.objects.filter(pk=2).last()
    photo3 = Photo.objects.filter(pk=3).last()
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]

    context = {
        'news': news,
        'username': username,
        'most_read': most_read,
        'comments': comments,
        'tag_news': tag_news,
        'related_news': related_news,
        'photo1': photo1,
        'photo2': photo2,
        'photo3': photo3,
        'photos': photos,
        'advertisings': advertisings,
    }
    return render(request, 'news-details.html', context)


# Add Comment to news
def postComment(request, pk):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        if ('comment' and 'email' and 'name') in request.POST:
            if (request.POST['comment'] != "") and (request.POST['email'] != "") and (
                    request.POST['name'] != "") and check(request.POST['email']):
                news = News.objects.filter(pk=pk).last()
                if news:
                    comment = Comment.objects.create(email=request.POST['email'], text=request.POST['comment'],
                                                     news=news, auther=request.POST['name'])
                    if comment:
                        return JsonResponse({"comment": "done"}, status=200)

    # some error occured
    return JsonResponse({"error": "من فضلك ادخل بيانات صحيحة"}, status=400)


# News page
def News_page(request, pk, page):
    category = Category.objects.filter(pk=pk).last()
    if category.name == 'عرب وعالم':
        news_list = News.objects.filter(
            Q(approval=True) & (Q(category__parent__name='عرب وعالم') | Q(category__name='عرب وعالم'))).order_by(
            '-Publish_date')
    elif category.name == 'محافظات':
        news_list = News.objects.filter(
            Q(approval=True) & (Q(category__parent__name='محافظات') | Q(category__name='محافظات'))).order_by(
            '-Publish_date')
    elif category.name == 'منوعات':
        news_list = News.objects.filter(
            Q(approval=True) & (Q(category__parent__name='منوعات') | Q(category__name='منوعات'))).order_by(
            '-Publish_date')
    elif category.name == 'ناس ومجتمع':
        news_list = News.objects.filter(
            Q(approval=True) & (Q(category__parent__name='ناس ومجتمع') | Q(category__name='ناس ومجتمع'))).order_by(
            '-Publish_date')
    elif category.name == 'صوت وصورة':
        news_list = News.objects.filter(
            Q(approval=True) & (Q(category__parent__name='صوت وصورة') | Q(category__name='صوت وصورة'))).order_by(
            '-Publish_date')
    elif category.name == 'عقارات وسيارات':
        news_list = News.objects.filter(Q(approval=True) & (
                Q(category__parent__name='عقارات وسيارات') | Q(category__name='عقارات وسيارات'))).order_by(
            '-Publish_date')
    elif category.name == 'مواهب وهويات':
        news_list = News.objects.filter(
            Q(approval=True) & (Q(category__parent__name='مواهب وهويات') | Q(category__name='مواهب وهويات'))).order_by(
            '-Publish_date')
    elif category.name == 'ثقافة وفنون':
        news_list = News.objects.filter(
            Q(approval=True) & (Q(category__parent__name='ثقافة وفنون') | Q(category__name='ثقافة وفنون'))).order_by(
            '-Publish_date')
    elif category.name == 'رياضة':
        news_list = News.objects.filter(
            Q(approval=True) & (Q(category__parent__name='رياضة') | Q(category__name='رياضة'))).order_by(
            '-Publish_date')
    elif category.name == 'سياسه وأقتصاد':
        news_list = News.objects.filter(Q(approval=True) & (
                Q(category__parent__name='سياسه وأقتصاد') | Q(category__name='سياسه وأقتصاد'))).order_by(
            '-Publish_date')
    elif category.name == 'حوادث وتحقيقات':
        news_list = News.objects.filter(Q(approval=True) & (
                Q(category__parent__name='حوادث وتحقيقات') | Q(category__name='حوادث وتحقيقات'))).order_by(
            '-Publish_date')
    else:
        news_list = News.objects.filter(category=category, approval=True)
    paginator = Paginator(news_list, 10)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    # Most read
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
    # Notes العناوين
    notes = Note.objects.all().order_by('-id')[:3]
    photo1 = Photo.objects.filter(pk=1).last()
    photo2 = Photo.objects.filter(pk=2).last()
    photo3 = Photo.objects.filter(pk=3).last()
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    context = {'news_list': news,
               'category': category,
               'most_read': most_read,
               'notes': notes,
               'photo1': photo1,
               'photo2': photo2,
               'photo3': photo3,
               'photos': photos,
               'advertisings': advertisings,
               }
    return render(request, 'news-page.html', context)


# News tag page
def News_tag(request, pk, page):
    tag = Tag.objects.filter(pk=pk).first()
    news_tag_list = Tag_news.objects.filter(tag=tag)
    paginator = Paginator(news_tag_list, 10)
    try:
        news_tags = paginator.page(page)
    except PageNotAnInteger:
        news_tags = paginator.page(1)
    except EmptyPage:
        news_tags = paginator.page(paginator.num_pages)
    # Most read
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]

    # Notes العناوين
    notes = Note.objects.all().order_by('-id')[:3]
    photo1 = Photo.objects.filter(pk=1).last()
    photo2 = Photo.objects.filter(pk=2).last()
    photo3 = Photo.objects.filter(pk=3).last()
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    context = {
        'news_tags': news_tags,
        'tag': tag,
        'most_read': most_read,
        'notes': notes,
        'photo1': photo1,
        'photo2': photo2,
        'photo3': photo3,
        'photos': photos,
        'advertisings': advertisings,
    }
    return render(request, 'news-tag.html', context)


def Who_us(request):
    return render(request, 'who-us.html')


def Search_news(request, page):
    if request.GET.get('search'):
        news = News.objects.filter(title__icontains=request.GET.get('search'))
        paginator = Paginator(news, 10)
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)
        # Most read
        most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
        # Notes العناوين
        notes = Note.objects.all().order_by('-id')[:3]
        photo1 = Photo.objects.filter(pk=1).last()
        photo2 = Photo.objects.filter(pk=2).last()
        photo3 = Photo.objects.filter(pk=3).last()
        photos = Photo.objects.all()[5:10]
        advertisings = Photo.objects.all()[10:15]
        context = {
            'news_list': news,
            'most_read': most_read,
            'notes': notes,
            'photo1': photo1,
            'photo2': photo2,
            'photo3': photo3,
            'photos': photos,
            'advertisings': advertisings,

        }
        return render(request, 'news-page.html', context)

    return redirect('home')


# Last news
def Last_news(request, page):
    news_list = News.objects.filter(approval=True).order_by('-id')
    paginator = Paginator(news_list, 10)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    # Most read
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
    # Notes العناوين
    notes = Note.objects.all().order_by('-id')[:3]
    photo1 = Photo.objects.filter(pk=1).last()
    photo2 = Photo.objects.filter(pk=2).last()
    photo3 = Photo.objects.filter(pk=3).last()
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]

    context = {'news_list': news,
               'most_read': most_read,
               'notes': notes,
               'photo1': photo1,
               'photo2': photo2,
               'photo3': photo3,
               'photos': photos,
               'advertisings': advertisings,
               }
    return render(request, 'last-news.html', context)


# Most read
def most_read(request, page):
    news_list = News.objects.filter(approval=True).order_by('-viewCount')
    paginator = Paginator(news_list, 10)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    # Notes العناوين
    notes = Note.objects.all().order_by('-id')[:3]
    photo1 = Photo.objects.filter(pk=1).last()
    photo2 = Photo.objects.filter(pk=2).last()
    photo3 = Photo.objects.filter(pk=3).last()
    last_news = News.objects.filter(approval=True).order_by('-id')[:6]
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    context = {'news_list': news,
               'last_news': last_news,
               'notes': notes,
               'photo1': photo1,
               'photo2': photo2,
               'photo3': photo3,
               'photos': photos,
               'advertisings': advertisings,
               }
    return render(request, 'most-read.html', context)


# Most comment
def most_comment(request, page):
    news_list = News.objects.filter(approval=True).order_by('-commentCount')
    paginator = Paginator(news_list, 10)
    try:
        news = paginator.page(page)
    except PageNotAnInteger:
        news = paginator.page(1)
    except EmptyPage:
        news = paginator.page(paginator.num_pages)

    # Notes العناوين
    notes = Note.objects.all().order_by('-id')[:3]
    photo1 = Photo.objects.filter(pk=1).last()
    photo2 = Photo.objects.filter(pk=2).last()
    photo3 = Photo.objects.filter(pk=3).last()
    last_news = News.objects.filter(approval=True).order_by('-id')[:6]
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]

    context = {'news_list': news,
               'last_news': last_news,
               'notes': notes,
               'photo1': photo1,
               'photo2': photo2,
               'photo3': photo3,
               'photos': photos,
               'advertisings': advertisings,
               }
    return render(request, 'most-comment.html', context)
