from django.shortcuts import render, redirect, get_object_or_404
from .models import News, Category, Note, Comment, Tag_news, Tag, Book, Carton, Video, Audio, TV
from django.db.models import Q
from django.core import serializers
from django.http import JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import re
from user.models import User, Photo, Advertising, Survey

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

    books1 = Book.objects.all().order_by('-Publish_date')[:5]
    books2 = Book.objects.all().order_by('-Publish_date')[5:10]
    # Most read الأكثر قراءه
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
    # Notes العناوين
    notes = Note.objects.all().order_by('-id')
    # Notes العناوين
    photo4 = Photo.objects.filter(pk=4).last()
    photo5 = Photo.objects.filter(pk=5).last()
    photos = Photo.objects.all()[5:]
    advertisings = Advertising.objects.all()
    cartons = Carton.objects.all()[:4]
    more_comments = News.objects.all().order_by('commentCount')[:6]
    # استطلاعات الرأى surveys
    surveys = Survey.objects.all()
    # Videos
    videos = Video.objects.all()[:2]
    # Audios
    audios = Audio.objects.all()
    # TV
    tvs = TV.objects.all()
    context = {
        'videos': videos,
        'audios': audios,
        'tvs': tvs,
        'latest_news': latest_news,
        'books1': books1,
        'books2': books2,
        'breaking_news0': breaking_news0,
        'breaking_news1': breaking_news1,
        'most_read': most_read,
        'notes': notes,
        'photo4': photo4,
        'photo5': photo5,
        'photos': photos,
        'advertisings': advertisings,
        'cartons': cartons,
        'more_comments': more_comments,
        'surveys': surveys,

    }
    return render(request, 'index.html', context)


# News details page
def News_details(request, pk):
    news = get_object_or_404(News, pk=pk)
    username = 'غير معروف'
    if news.user:
        name = get_object_or_404(User, id=news.user.id)
        username = name.name
    if news.approval == False:
        if request.user.is_authenticated:
            my_user = get_object_or_404(User, id=request.user.id)
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
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]

    context = {
        'news': news,
        'username': username,
        'most_read': most_read,
        'comments': comments,
        'tag_news': tag_news,
        'related_news': related_news,
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
    category = get_object_or_404(Category, pk=pk)
    news_list = category.all_news()
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
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    context = {
        'news_list': news,
        'category': category,
        'most_read': most_read,
        'notes': notes,
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
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    context = {
        'news_tags': news_tags,
        'tag': tag,
        'most_read': most_read,
        'notes': notes,
        'photos': photos,
        'advertisings': advertisings,
    }
    return render(request, 'news-tag.html', context)


def Who_us(request):
    return render(request, 'who-us.html')


def post_your_photo(request):
    # Notes العناوين
    notes = Note.objects.all().order_by('-id')[:3]
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    return render(request, 'post-your-photo.html', {
        'notes': notes,
        'photos': photos,
        'advertisings': advertisings,
    })


def Search_news(request, page):
    news = News.objects.all()
    search = 'الكل'
    if request.GET.get('search'):
        search = request.GET.get('search')
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
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    context = {
        'search': search,
        'news_list': news,
        'most_read': most_read,
        'notes': notes,
        'photos': photos,
        'advertisings': advertisings,
    }
    return render(request, 'search-news.html', context)


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
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]

    context = {
        'news_list': news,
        'most_read': most_read,
        'notes': notes,
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
    last_news = News.objects.filter(approval=True).order_by('-id')[:6]
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    context = {
        'news_list': news,
        'last_news': last_news,
        'notes': notes,
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
    last_news = News.objects.filter(approval=True).order_by('-id')[:6]
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]

    context = {
        'news_list': news,
        'last_news': last_news,
        'notes': notes,
        'photos': photos,
        'advertisings': advertisings,
    }
    return render(request, 'most-comment.html', context)


def create_category(request):
    if Category.objects.all().count() == 0:
        Category.objects.create(name='محليات')
        arab_and_world = Category.objects.create(name='عرب وعالم')
        Category.objects.create(name='عرب', parent=arab_and_world)
        Category.objects.create(name='عالم', parent=arab_and_world)
        Category.objects.create(name='افريقا', parent=arab_and_world)
        Category.objects.create(name='الصين', parent=arab_and_world)
        accidents_and_talents = Category.objects.create(name='حوادث وتحقيقات')
        Category.objects.create(name='حوادث', parent=accidents_and_talents)
        Category.objects.create(name='تحقيقات', parent=accidents_and_talents)
        Category.objects.create(name='ملفات ساخنة', parent=accidents_and_talents)
        Category.objects.create(name='جرائم', parent=accidents_and_talents)
        Category.objects.create(name='محاكم', parent=accidents_and_talents)
        politics_and_economy = Category.objects.create(name='سياسة واقتصاد')
        Category.objects.create(name='اسعار واسواق', parent=politics_and_economy)
        Category.objects.create(name='بورصة وشركات', parent=politics_and_economy)
        Category.objects.create(name='بنوك واستثمار', parent=politics_and_economy)
        Category.objects.create(name='نقل وملاحة', parent=politics_and_economy)
        sport = Category.objects.create(name='رياضة')
        Category.objects.create(name='رياضة محلية', parent=sport)
        Category.objects.create(name='رياضة عربية', parent=sport)
        Category.objects.create(name='رياضة عالمية', parent=sport)
        culture_and_arts = Category.objects.create(name='ثقافة وفنون')
        Category.objects.create(name='تراث', parent=culture_and_arts)
        Category.objects.create(name='اعلام', parent=culture_and_arts)
        Category.objects.create(name='اصدارات', parent=culture_and_arts)
        Category.objects.create(name='كاركاتير', parent=culture_and_arts)
        Category.objects.create(name='كتب', parent=culture_and_arts)
        Category.objects.create(name='ثقافات', parent=culture_and_arts)
        Category.objects.create(name='نصوص', parent=culture_and_arts)
        Category.objects.create(name='فنون', parent=culture_and_arts)
        Category.objects.create(name='اراء ومقالات', parent=culture_and_arts)
        Category.objects.create(name='بورتريه', parent=culture_and_arts)
        talents_and_hobbies = Category.objects.create(name='مواهب وهوايات')
        Category.objects.create(name='مواهب', parent=talents_and_hobbies)
        Category.objects.create(name='غرائب وطرائف', parent=talents_and_hobbies)
        Category.objects.create(name='مسابقات وتسالى', parent=talents_and_hobbies)
        Category.objects.create(name='هوايات', parent=talents_and_hobbies)
        buildings = Category.objects.create(name='عقارات')
        cars = Category.objects.create(name='سيارات')
        buildings_and_cars = Category.objects.create(name='عقارات وسيارات')
        cars.parent = buildings_and_cars
        cars.save()
        buildings.parent = buildings_and_cars
        buildings.save()
        video_and_audio = Category.objects.create(name='صوت وصورة')
        Category.objects.create(name='فيديوهات', parent=video_and_audio)
        Category.objects.create(name='ألبومات صور', parent=video_and_audio)
        Category.objects.create(name='راديو الأستاذ', parent=video_and_audio)
        Category.objects.create(name='تليفزيون الأستاذ', parent=video_and_audio)
        people_and_society = Category.objects.create(name='ناس ومجتمع')
        Category.objects.create(name='انفوجراف', parent=people_and_society)
        Category.objects.create(name='حياة كريمة', parent=people_and_society)
        Category.objects.create(name='خدمات وأدلة', parent=people_and_society)
        Category.objects.create(name='حياة الناس', parent=people_and_society)
        Category.objects.create(name='أهل الخير', parent=people_and_society)
        Category.objects.create(name='وفيات', parent=people_and_society)
        Category.objects.create(name='مفقودات', parent=people_and_society)
        Category.objects.create(name='تهانى ومناسبات', parent=people_and_society)
        Category.objects.create(name='الصلح خير', parent=people_and_society)
        Category.objects.create(name='خطابك وصل', parent=people_and_society)
        Category.objects.create(name='تسالى وابتسامات', parent=people_and_society)
        Category.objects.create(name='مخترعات وابتكارات', parent=people_and_society)
        Category.objects.create(name='استغاثات ومتابعات', parent=people_and_society)
        Category.objects.create(name='جمعيات ونقابات', parent=people_and_society)
        Category.objects.create(name='حدوتة مصرية', parent=people_and_society)
        mix = Category.objects.create(name='منوعات')
        Category.objects.create(name='سيدتى وطفلك', parent=mix)
        Category.objects.create(name='خدمات ومجتمع', parent=mix)
        Category.objects.create(name='كاريكاتير ورسوم', parent=mix)
        Category.objects.create(name='صحافة و تليفزيون', parent=mix)
        Category.objects.create(name='علوم وتكنولوجيا', parent=mix)
        Category.objects.create(name='صحة وجمال', parent=mix)
        Category.objects.create(name='صور وفيديوهات', parent=mix)
        Category.objects.create(name='تريندات وهاشتاجات عربية', parent=mix)
        advertising_and_advertisements = Category.objects.create(name='دعاية وإعلانات', parent=mix)
        Category.objects.create(name='أسواق ومعارض', parent=advertising_and_advertisements)
        Category.objects.create(name='عروض وخصومات', parent=advertising_and_advertisements)
        Category.objects.create(name='شركات ومصانع', parent=advertising_and_advertisements)
        Category.objects.create(name='تدريب وتسويق', parent=advertising_and_advertisements)
        Category.objects.create(name='تأمين واستثمار', parent=advertising_and_advertisements)
        Category.objects.create(name='محلات تجارية وافتتاحات', parent=advertising_and_advertisements)
        governments = Category.objects.create(name='محافظات')
        Category.objects.create(name='الوادي الجديد', parent=governments)
        Category.objects.create(name='المنيا', parent=governments)
        Category.objects.create(name='المنوفية', parent=governments)
        Category.objects.create(name='مرسى مطروح', parent=governments)
        Category.objects.create(name='كفر الشيخ', parent=governments)
        Category.objects.create(name='قنا', parent=governments)
        Category.objects.create(name='القليوبية', parent=governments)
        Category.objects.create(name='القاهرة', parent=governments)
        Category.objects.create(name='الفيوم', parent=governments)
        Category.objects.create(name='الغربية', parent=governments)
        Category.objects.create(name='شمال سينا', parent=governments)
        Category.objects.create(name='الشرقية', parent=governments)
        Category.objects.create(name='السويس', parent=governments)
        Category.objects.create(name='سوهاج', parent=governments)
        Category.objects.create(name='دمياط', parent=governments)
        Category.objects.create(name='الدقهليه', parent=governments)
        Category.objects.create(name='الجيزة', parent=governments)
        Category.objects.create(name='جنوب سينا', parent=governments)
        Category.objects.create(name='بورسعيد', parent=governments)
        Category.objects.create(name='بني سويف', parent=governments)
        Category.objects.create(name='البحيرة', parent=governments)
        Category.objects.create(name='البحر الاحمر', parent=governments)
        Category.objects.create(name='الاقصر', parent=governments)
        Category.objects.create(name='اسيوط', parent=governments)
        Category.objects.create(name='اسوان', parent=governments)
        Category.objects.create(name='الاسماعلية', parent=governments)
        Category.objects.create(name='الاسكندرية', parent=governments)
        more = Category.objects.create(name='المزيد')
        Category.objects.create(name='عاجل', parent=more)
        Category.objects.create(name='دنيا ودين', parent=more)
        Category.objects.create(name='سياحة وطيران', parent=more)
        Category.objects.create(name='فيروس كورونا', parent=more)
        Category.objects.create(name='قنصليات وسفارات', parent=more)
        return redirect('home')
    else:
        return redirect('home')


def make_survey(request, pk):
    # Most read الأكثر قراءه
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    survey = get_object_or_404(Survey, pk=pk)
    if request.POST:
        if 'survey' in request.POST:
            if request.POST['survey'] == 'yes':
                survey.yes += 1
                survey.all += 1
            elif request.POST['survey'] == 'no':
                survey.no += 1
                survey.all += 1
            survey.save()
    context = {
        'most_read': most_read,
        'photos': photos,
        'advertisings': advertisings,
        'survey': survey,

    }
    return render(request, 'make_survey.html', context)


# book details page
def book_details(request, pk):
    book = get_object_or_404(Book, pk=pk)
    # To increament book count
    book.incrementViewCount()
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]

    context = {
        'book': book,
        'most_read': most_read,
        'photos': photos,
        'advertisings': advertisings,
    }
    return render(request, 'book-details.html', context)


# News page
def books_page(request, page):
    news_list = Book.objects.all()
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
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    context = {
        'news_list': news,
        'most_read': most_read,
        'notes': notes,
        'photos': photos,
        'advertisings': advertisings,
    }
    return render(request, 'books-page.html', context)


# News page
def cartons_page(request, page):
    news_list = Carton.objects.all()
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
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    context = {
        'news_list': news,
        'most_read': most_read,
        'notes': notes,
        'photos': photos,
        'advertisings': advertisings,
    }
    return render(request, 'cartons-page.html', context)


# News details page
def carton_details(request, pk):
    news = get_object_or_404(Carton, pk=pk)
    # To increament news count
    news.incrementViewCount()
    # Most read الأكثر قراءه
    most_read = News.objects.filter(approval=True).order_by('-viewCount', '-Publish_date')[:6]
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]

    context = {
        'news': news,
        'most_read': most_read,
        'photos': photos,
        'advertisings': advertisings,
    }
    return render(request, 'carton-details.html', context)


# News page
def videos_page(request, page):
    news_list = Video.objects.all()
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
    photos = Photo.objects.all()[5:10]
    advertisings = Photo.objects.all()[10:15]
    context = {
        'news_list': news,
        'most_read': most_read,
        'notes': notes,
        'photos': photos,
        'advertisings': advertisings,
    }
    return render(request, 'videos-page.html', context)
