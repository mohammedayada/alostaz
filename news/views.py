from django.shortcuts import render
from .models import News, Category, Photo, Note
from django.db.models import Q
# Create your views here.
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
    arab = Category.objects.filter(name='عرب').last()
    world = Category.objects.filter(name='عالم').last()
    africa = Category.objects.filter(name='أفريقيا').last()
    china = Category.objects.filter(name='الصين').last()
    arabs_worlds = Category.objects.filter(name='عرب وعالم').last()
    arab_and_world = News.objects.filter(
        Q(approval=True) &
        (Q(category=arab) | Q(category=world) | Q(category=africa) | Q(category=china) | Q(category=arabs_worlds))).order_by('-Publish_date')[:9]

    # حوادث وتحقيقات Accidents and investigations
    accidents = Category.objects.filter(name='حوادث').last()
    investigations = Category.objects.filter(name='تحقيقات').last()
    hot_files = Category.objects.filter(name='ملفات ساخنه').last()
    crimes = Category.objects.filter(name='جرائم').last()
    courts = Category.objects.filter(name='محاكم').last()
    accidents_investigations = Category.objects.filter(name='حوادث وتحقيقات').last()
    accidents_and_investigations = News.objects.filter(
        Q(approval=True) &
        (Q(category=accidents)
         | Q(category=investigations)
         | Q(category=hot_files)
         | Q(category=crimes)
         | Q(category=courts)
         | Q(category=accidents_investigations))).order_by('-Publish_date')[:9]

    # Politics and Economy سياسه واقتصاد
    prices_and_markets = Category.objects.filter(name='أسعار وأسواق').last()
    stock_exchange_and_companies = Category.objects.filter(name='بورصة وشركات').last()
    banking_and_investment = Category.objects.filter(name='بنوك وأستثمار').last()
    transport_and_navigation = Category.objects.filter(name='نقل وملاحة').last()
    politics_economies = Category.objects.filter(name='سياسة وأقتصاد').last()
    politics_and_economy = News.objects.filter(
        Q(approval=True) &
        (Q(category=prices_and_markets)
         | Q(category=stock_exchange_and_companies)
         | Q(category=banking_and_investment)
         | Q(category=transport_and_navigation)
         | Q(category=politics_economies))).order_by('-Publish_date')[:9]

    # sport رياضة
    local_sports = Category.objects.filter(name='رياضة محلية').last()
    arab_sports = Category.objects.filter(name='رياضة عربية').last()
    world_sport = Category.objects.filter(name='رياضة عالمية').last()
    sport = Category.objects.filter(name='رياضة').last()
    sports = News.objects.filter(
        Q(approval=True) &
        (Q(category=local_sports)
         | Q(category=arab_sports)
         | Q(category=world_sport)
         | Q(category=sport))).order_by('-Publish_date')[:9]
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
        'breaking_news0': breaking_news0,
        'breaking_news1': breaking_news1,
        'most_read': most_read,
        'images': images,
        'notes': notes,
               }
    return render(request, 'index.html', context)
