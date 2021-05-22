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

    # Culture and arts ثقافه وفنون
    portrait = Category.objects.filter(name='بورترية').last()
    heritage = Category.objects.filter(name='تراث').last()
    information = Category.objects.filter(name='اعلام').last()
    publications = Category.objects.filter(name='اصدارات').last()
    caricature = Category.objects.filter(name='كاركاتير').last()
    books = Category.objects.filter(name='كتب').last()
    cultures = Category.objects.filter(name='ثقافات').last()
    texts = Category.objects.filter(name='نصوص').last()
    arts = Category.objects.filter(name='فنون').last()
    reviews_and_articles = Category.objects.filter(name='اراء ومقالات').last()
    cultures_arts = Category.objects.filter(name='ثقافة وفنون').last()
    culture_and_arts = News.objects.filter(
        Q(approval=True) &
        (Q(category=portrait)
         | Q(category=heritage)
         | Q(category=information)
         | Q(category=publications)
         | Q(category=caricature)
         | Q(category=books)
         | Q(category=cultures)
         | Q(category=texts)
         | Q(category=arts)
         | Q(category=reviews_and_articles)
         | Q(category=cultures_arts))).order_by('-Publish_date')[:9]

    # Talents and identities مواهب وهوايات
    talents = Category.objects.filter(name='مواهب').last()
    identities = Category.objects.filter(name='هوايات').last()
    oddity_and_odds = Category.objects.filter(name='غرائب وطرائف').last()
    contests_and_fun = Category.objects.filter(name='مسابقات وتسالى').last()
    talents_identities = Category.objects.filter(name='مواهب وهوايات').last()
    talents_and_identities = News.objects.filter(
        Q(approval=True) &
        (Q(category=talents)
         | Q(category=identities)
         | Q(category=oddity_and_odds)
         | Q(category=contests_and_fun)
         | Q(category=talents_identities))).order_by('-Publish_date')[:9]
    # Real Estate and Cars عقارات وسيارات
    real_estate = Category.objects.filter(name='عقارات').last()
    cars = Category.objects.filter(name='سيارات').last()
    real_estate_cars = Category.objects.filter(name='عقارات وسيارات').last()
    real_estate_and_cars = News.objects.filter(
        Q(approval=True) &
        (Q(category=real_estate)
         | Q(category=cars)
         | Q(category=real_estate_cars))).order_by('-Publish_date')[:9]
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
        'breaking_news0': breaking_news0,
        'breaking_news1': breaking_news1,
        'most_read': most_read,
        'images': images,
        'notes': notes,
               }
    return render(request, 'index.html', context)
