from django.shortcuts import render
from .models import News, Category, Photo, Note, Comment, Tag_news, Tag
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re

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
    # Most read الأكثر قراءه
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
    # Images الصور
    images = Photo.objects.all().order_by('-id')[:4]
    # Notes العناوين
    notes = Note.objects.all().order_by('-id')[:10]
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
        'breaking_news0': breaking_news0,
        'breaking_news1': breaking_news1,
        'most_read': most_read,
        'images': images,
        'notes': notes,
    }
    return render(request, 'index.html', context)


# News details page
def News_details(request, pk):
    news = News.objects.filter(pk=pk).last()
    # To increament news count
    news.incrementViewCount()
    # Most read الأكثر قراءه
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
    # comments for this post
    comments = Comment.objects.filter(news=news, approval=True)
    # Tags
    tag_news = Tag_news.objects.filter(news=news)
    # Related News الموضوعات المتعلقه
    related_news = News.objects.filter(Q(approval=True) & Q(category=news.category) & ~Q(pk=news.pk)).order_by('-Publish_date')[:3]

    context = {
        'news': news,
        'most_read': most_read,
        'comments': comments,
        'tag_news': tag_news,
        'related_news': related_news
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

    context = {'news_list': news,
               'category': category,
               'most_read': most_read,
               'notes': notes,
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
    context = {
        'news_tags': news_tags,
        'tag': tag,
        'most_read': most_read,
        'notes': notes,
               }
    return render(request, 'news-tag.html', context)
