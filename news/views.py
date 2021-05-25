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

# Arab and world
def arabs_worldss():
    # Arabs and the world عرب وعالم
    arab = Category.objects.filter(name='عرب').last()
    world = Category.objects.filter(name='عالم').last()
    africa = Category.objects.filter(name='أفريقيا').last()
    china = Category.objects.filter(name='الصين').last()
    arabs_worlds = Category.objects.filter(name='عرب وعالم').last()
    return News.objects.filter(
        Q(approval=True) &
        (Q(category=arab) | Q(category=world) | Q(category=africa) | Q(category=china) | Q(
            category=arabs_worlds))).order_by('-Publish_date')

# Cites
def citess():
    city = Category.objects.filter(name='محافظات').last()
    new_vally = Category.objects.filter(name='الوادي الجديد').last()
    elmenia = Category.objects.filter(name='المنيا').last()
    elmonofia = Category.objects.filter(name='المنوفية').last()
    matroh = Category.objects.filter(name='مرسى مطروح').last()
    kafr_elshikh = Category.objects.filter(name='كفر الشيخ').last()
    qena = Category.objects.filter(name='قنا').last()
    qaliob = Category.objects.filter(name='القليوبية').last()
    cairo = Category.objects.filter(name='القاهرة').last()
    elfaiom = Category.objects.filter(name='الفيوم').last()
    elghrbia = Category.objects.filter(name='الغربية').last()
    sina_north = Category.objects.filter(name='شمال سينا').last()
    elsharkia = Category.objects.filter(name='الشرقية').last()
    elswis = Category.objects.filter(name='السويس').last()
    sohag = Category.objects.filter(name='سوهاج').last()
    demiat = Category.objects.filter(name='دمياط').last()
    eldakhlia = Category.objects.filter(name='الدقهليه').last()
    elgiza = Category.objects.filter(name='الجيزة').last()
    sina_east = Category.objects.filter(name='جنوب سينا').last()
    porsaid = Category.objects.filter(name='بورسعيد').last()
    baniswif = Category.objects.filter(name='بني سويف').last()
    elbhira = Category.objects.filter(name='البحيرة').last()
    red_sea = Category.objects.filter(name='البحر الاحمر').last()
    louxer = Category.objects.filter(name='الاقصر').last()
    assiut = Category.objects.filter(name='اسيوط').last()
    aswan = Category.objects.filter(name='اسوان').last()
    ismalia = Category.objects.filter(name='الاسماعلية').last()
    alex = Category.objects.filter(name='الاسكندرية').last()

    cites = News.objects.filter(
        Q(approval=True) &
        (Q(category=city)
         | Q(category=new_vally)
         | Q(category=elbhira)
         | Q(category=elgiza)
         | Q(category=elswis)
         | Q(category=eldakhlia)
         | Q(category=elmenia)
         | Q(category=elsharkia)
         | Q(category=elmonofia)
         | Q(category=kafr_elshikh)
         | Q(category=alex)
         | Q(category=aswan)
         | Q(category=assiut)
         | Q(category=ismalia)
         | Q(category=baniswif)
         | Q(category=louxer)
         | Q(category=red_sea)
         | Q(category=porsaid)
         | Q(category=sohag)
         | Q(category=sina_north)
         | Q(category=sina_east)
         | Q(category=matroh)
         | Q(category=qena)
         | Q(category=demiat)
         | Q(category=qaliob)
         | Q(category=cairo)
         | Q(category=elfaiom)
         | Q(category=elghrbia)))
    return cites

# mix
def mixss():
    mix = Category.objects.filter(name='منوعات').last()
    madam_and_services = Category.objects.filter(name='سيدتى وطفلك').last()
    services_and_society = Category.objects.filter(name='خدمات ومجتمع').last()
    cartons = Category.objects.filter(name='كاركاتير ورسوم').last()
    press_and_TV = Category.objects.filter(name='صحافة وتلفزيون').last()
    science_and_technology = Category.objects.filter(name='علوم وتكنولوجيا').last()
    health_and_beauty = Category.objects.filter(name='صحة وجمال').last()
    photos_and_videos = Category.objects.filter(name='صور وفيديوهات').last()
    trends_and_hashtags_arab = Category.objects.filter(name='تريندات وهاشتجات عربية').last()
    advertising = Category.objects.filter(name='دعاية واعلان').last()
    markets_and_fairs = Category.objects.filter(name='أسواق ومعارض').last()
    offers_and_discounts = Category.objects.filter(name='عروض وخصومات').last()
    campanies_and_factories = Category.objects.filter(name='شركات ومصانع').last()
    training_and_marketing = Category.objects.filter(name='تدريب وتسويق').last()
    insurance_and_investment = Category.objects.filter(name='تأمين واستثمار').last()
    shops_and_openings = Category.objects.filter(name='محلات تجارية وافتتاحات').last()
    mixs = News.objects.filter(
        Q(approval=True) &
        (Q(category=mix)
         | Q(category=madam_and_services)
         | Q(category=services_and_society)
         | Q(category=cartons)
         | Q(category=press_and_TV)
         | Q(category=science_and_technology)
         | Q(category=health_and_beauty)
         | Q(category=photos_and_videos)
         | Q(category=trends_and_hashtags_arab)
         | Q(category=advertising)
         | Q(category=markets_and_fairs)
         | Q(category=offers_and_discounts)
         | Q(category=campanies_and_factories)
         | Q(category=training_and_marketing)
         | Q(category=insurance_and_investment)
         | Q(category=shops_and_openings)))
    return mixs

# ناس ومجتمع
def peoples_and_societys():
    peoples_society = Category.objects.filter(name='ناس ومجتمع').last()
    infograph = Category.objects.filter(name='انفوجراف').last()
    good_life = Category.objects.filter(name='حياة كريمة').last()
    services_and_guides = Category.objects.filter(name='خدمات وأدلة').last()
    peoples_life = Category.objects.filter(name='حياة الناس').last()
    people_of_goodness = Category.objects.filter(name='أهل الخير').last()
    mortality = Category.objects.filter(name='وفيات').last()
    lost = Category.objects.filter(name='مفقودات').last()
    congratulations_and_happiness = Category.objects.filter(name='تهانى ومناسبات').last()
    solvency_is_good = Category.objects.filter(name='الصلح خير').last()
    your_letter_is_arrived = Category.objects.filter(name='خطابك وصل').last()
    good_fun_and_smiles = Category.objects.filter(name='تسالى وابتسامات').last()
    inventions_and_innovations = Category.objects.filter(name='مخترعات وابتكارات').last()
    distress_and_follow_up = Category.objects.filter(name='استغاثات ومتابعات').last()
    associations_and_unions = Category.objects.filter(name='جمعيات ونقابات').last()
    his_shoe_is_egyptian = Category.objects.filter(name='حدوتة مصرية').last()
    people_and_society = News.objects.filter(
        Q(approval=True) &
        (Q(category=peoples_society)
         | Q(category=infograph)
         | Q(category=good_life)
         | Q(category=services_and_guides)
         | Q(category=peoples_life)
         | Q(category=people_of_goodness)
         | Q(category=mortality)
         | Q(category=lost)
         | Q(category=congratulations_and_happiness)
         | Q(category=solvency_is_good)
         | Q(category=your_letter_is_arrived)
         | Q(category=good_fun_and_smiles)
         | Q(category=inventions_and_innovations)
         | Q(category=distress_and_follow_up)
         | Q(category=associations_and_unions)
         | Q(category=his_shoe_is_egyptian)))
    return people_and_society

#صوت وصوره
def video_and_audios():
    video = Category.objects.filter(name='فيديوهات').last()
    photo_albums = Category.objects.filter(name='البومات صور').last()
    professor_audio = Category.objects.filter(name='راديو الأستاذ').last()
    professor_Tv = Category.objects.filter(name='تلفزيون الأستاذ').last()
    videos_audios = Category.objects.filter(name='صوت وصورة').last()
    video_and_audio = News.objects.filter(
        Q(approval=True) &
        (Q(category=video)
         | Q(category=photo_albums)
         | Q(category=professor_audio)
         | Q(category=professor_Tv)
         | Q(category=videos_audios)))
    return video_and_audio

# عقارات وسيارات
def real_estate_and_carss():
    real_estate = Category.objects.filter(name='عقارات').last()
    cars = Category.objects.filter(name='سيارات').last()
    real_estate_cars = Category.objects.filter(name='عقارات وسيارات').last()
    real_estate_and_cars = News.objects.filter(
        Q(approval=True) &
        (Q(category=real_estate)
         | Q(category=cars)
         | Q(category=real_estate_cars))).order_by('-Publish_date')
    return real_estate_and_cars

# مواهب وهويات
def talents_and_identitiess():
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
         | Q(category=talents_identities))).order_by('-Publish_date')
    return talents_and_identities

def culture_and_artss():
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
         | Q(category=cultures_arts))).order_by('-Publish_date')
    return culture_and_arts

def sportss():
    local_sports = Category.objects.filter(name='رياضة محلية').last()
    arab_sports = Category.objects.filter(name='رياضة عربية').last()
    world_sport = Category.objects.filter(name='رياضة عالمية').last()
    sport = Category.objects.filter(name='رياضة').last()
    sports = News.objects.filter(
        Q(approval=True) &
        (Q(category=local_sports)
         | Q(category=arab_sports)
         | Q(category=world_sport)
         | Q(category=sport))).order_by('-Publish_date')
    return sports
def politics_and_economys():
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
         | Q(category=politics_economies))).order_by('-Publish_date')
    return politics_and_economy


def accidents_and_investigationss():
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
         | Q(category=accidents_investigations))).order_by('-Publish_date')
    return accidents_and_investigations


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
    arab_and_world = arabs_worldss()[:9]
    # حوادث وتحقيقات Accidents and investigations
    accidents_and_investigations = accidents_and_investigationss()[:9]
    # Politics and Economy سياسه واقتصاد
    politics_and_economy = politics_and_economys()[:9]
    # sport رياضة
    sports = sportss()[:9]

    # Culture and arts ثقافه وفنون
    culture_and_arts = culture_and_artss()[:9]
    # Talents and identities مواهب وهوايات
    talents_and_identities = talents_and_identitiess()[:9]
    # Real Estate and Cars عقارات وسيارات
    real_estate_and_cars = real_estate_and_carss()[:9]
    # Video and audio صوت وصوره
    video_and_audio = video_and_audios()[:9]
    # ناس ومجتمع
    people_and_society = peoples_and_societys()[:9]
    # منوعات
    mixs = mixss()[:9]
    # محافظات cites
    cites = citess()[:9]
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

    context = {
        'news': news,
        'most_read': most_read,
        'comments': comments,
        'tag_news': tag_news,
    }
    return render(request, 'news-details.html', context)

# Add Comment to news
def postComment(request, pk):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        if ('comment' and 'email' and 'name') in request.POST:
            if (request.POST['comment']!="") and (request.POST['email']!="") and (request.POST['name']!="") and check(request.POST['email']):
                news = News.objects.filter(pk=pk).last()
                if news:
                    comment = Comment.objects.create(email=request.POST['email'], text=request.POST['comment'], news=news, auther=request.POST['name'])
                    if comment:
                        return JsonResponse({"comment": "done"}, status=200)

    # some error occured
    return JsonResponse({"error": "من فضلك ادخل بيانات صحيحة"}, status=400)

# News page
def News_page(request, pk, page):
    category = Category.objects.filter(pk=pk).last()
    if category.name =='عرب وعالم':
        news_list = arabs_worldss()
    elif category.name =='محافظات':
        news_list = citess()
    elif category.name =='منوعات':
        news_list = mixss()
    elif category.name =='ناس ومجتمع':
        news_list = peoples_and_societys()
    elif category.name == 'صوت وصورة':
        news_list = video_and_audios()
    elif category.name == 'عقارات وسيارات':
        news_list = real_estate_and_carss()
    elif category.name == 'مواهب وهويات':
        news_list = talents_and_identitiess()
    elif category.name == 'ثقافة وفنون':
        news_list = culture_and_artss()
    elif category.name == 'رياضة':
        news_list = sportss()
    elif category.name == 'سياسه وأقتصاد':
        news_list = politics_and_economys()
    elif category.name == 'حوادث وتحقيقات':
        news_list = accidents_and_investigationss()
    else:
        news_list = News.objects.filter(category=category)
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