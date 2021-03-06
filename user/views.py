from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import (
    User,
    Photo,
    Advertising,
    Subscriber,
    Survey
)
from news.models import (
    Note,
    Tag,
    News,
    Category,
    Comment,
    Tag_news,
    Book,
    Video,
    Audio,
    TV
)
from .forms import (
    NewsForm,
    PhotoForm,
    AdvertisingForm,
    SurveyForm,
    CategoryForm,
    BookForm,
    VideoForm,
    AudioForm,
    TVForm
)
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import JsonResponse
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


# login function
def user_login(request):
    # when request POST
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('show-news', page=1)

    return redirect('home')


# logout function
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')


# add user
@login_required
def add_user(request):
    # when request POST
    if request.user.type == 'chairman':
        msg = 'من فضلك ادخل بيانات صحيحه'
        if request.POST:
            if request.POST['email'] != "" and request.POST['name'] != "" and request.POST['password'] != "" and \
                    request.POST['type'] != "" and request.POST['phone'] != "":
                if User.objects.filter(email=request.POST['email']).count() == 0:
                    new_user = User.objects.create_user(
                        name=request.POST['name'],
                        email=request.POST['email'],
                        phone=request.POST['phone'],
                        type=request.POST['type'],
                        password=request.POST['password'],
                        is_active=True,
                    )
                    if request.POST['type'] == 'chairman':
                        new_user.is_superuser = True
                        new_user.save()
                    return redirect('show-users', page=1)
                else:
                    msg = 'من فضلك ادخل بريد الكترونى صحيح'
        context = {'msg': msg,
                   }
        return render(request, 'dashboard/add_user.html', context)
    else:
        return redirect('home')


# Show user
@login_required
def show_users(request, page):
    if request.user.type == 'chairman':
        users = User.objects.all()
        if request.GET.get('search'):
            users = User.objects.filter(name__icontains=request.GET.get('search'))
        paginator = Paginator(users, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        context = {'users': users,
                   }
        return render(request, 'dashboard/show_users.html', context)
    else:
        return redirect('home')


@login_required
def add_note(request):
    # when request POST
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        msg = 'من فضلك ادخل بيانات صحيحه'
        if request.POST:
            if request.POST['title'] != "" and request.POST['link'] != "":
                Note.objects.create(
                    user=request.user,
                    title=request.POST['title'],
                    link=request.POST['link'],
                )
                return redirect('show-notes', page=1)
        context = {'msg': msg,
                   }
        return render(request, 'dashboard/add_note.html', context)
    else:
        return redirect('home')


# Show user
@login_required
def show_notes(request, page):
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        notes = Note.objects.all()
        paginator = Paginator(notes, 10)
        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)
        context = {'notes': notes,
                   }
        return render(request, 'dashboard/show_notes.html', context)
    else:
        return redirect('home')


@login_required
def add_tag(request):
    # when request POST
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        msg = 'من فضلك ادخل بيانات صحيحه'
        if request.POST:
            if request.POST['text'] != "":
                if Tag.objects.filter(text=request.POST['text']).count() == 0:
                    Tag.objects.create(
                        text=request.POST['text'],
                    )
                    return redirect('show-tags', page=1)
                msg = 'هذه الكلمه الدلاليه موجوده بالفعل'
        context = {'msg': msg,
                   }
        return render(request, 'dashboard/add_tag.html', context)
    else:
        return redirect('home')


# Show tags
@login_required
def show_tags(request, page):
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        tags = Tag.objects.all()
        if request.GET.get('search'):
            tags = Tag.objects.filter(text__icontains=request.GET.get('search'))
        paginator = Paginator(tags, 10)
        try:
            tags = paginator.page(page)
        except PageNotAnInteger:
            tags = paginator.page(1)
        except EmptyPage:
            tags = paginator.page(paginator.num_pages)
        context = {'tags': tags,
                   }
        return render(request, 'dashboard/show_tags.html', context)
    else:
        return redirect('home')


# Add news
@login_required
def add_news(request):
    context = {}
    form = NewsForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        # save the form data to model
        category = Category.objects.filter(id=request.POST['category']).last()
        News.objects.create(img=request.FILES['img'], title=request.POST['title'], category=category,
                            user=request.user, details=request.POST['details'])
        return redirect('show-news', page=1)
    context['form'] = form
    return render(request, 'dashboard/add_news.html', context)


# ِshow news
@login_required
def show_news(request, page):
    cond = True
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        news_list = News.objects.filter(approval=False)
    elif request.user.type == 'editor':
        news_list = News.objects.filter(approval=False, user=request.user)
    else:
        news_list = News.objects.filter(approval=False, user=request.user)
        cond = False
    paginator = Paginator(news_list, 10)
    try:
        news_list = paginator.page(page)
    except PageNotAnInteger:
        news_list = paginator.page(1)
    except EmptyPage:
        news_list = paginator.page(paginator.num_pages)

    context = {
        'cond': cond,
        'news_list': news_list,
    }
    return render(request, 'dashboard/show_news.html', context)


# Approve news
@login_required
def approve_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        news.approval = True
        news.save()
        return redirect('news_details', pk=pk)
    elif request.user.type == 'editor':
        news = News.objects.filter(approval=False, user=request.user).last()
        news.approval = True
        news.save()
        return redirect('news_details', pk=pk)
    else:
        return redirect('home')


# delete news
@login_required
def delete_news(request, pk):
    news = get_object_or_404(News, pk=pk)
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        news.delete()
        return redirect('show-news', page=1)
    elif request.user.type == 'editor':
        news = News.objects.filter(approval=False, user=request.user).last()
        news.delete()
        return redirect('show-news', page=1)
    else:
        return redirect('home')


# Edit news
@login_required
def edit_news(request, pk):
    context = {}
    news = get_object_or_404(News, pk=pk)
    cond = News.objects.filter(pk=pk, user=request.user).count()
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief' or cond > 0:
        context['news'] = news
        if request.POST:
            category = Category.objects.filter(id=request.POST['category']).last()
            if 'img' in request.FILES:
                news.img = request.FILES['img']
            news.title = request.POST['title']
            news.category = category
            news.details = request.POST['details']
            news.save()
            return redirect('news_details', pk=pk)
        else:
            form = NewsForm(instance=news)
            context['form'] = form
        return render(request, 'dashboard/edit_news.html', context)
    return redirect('news_details', pk=pk)


# ِshow comments
@login_required
def show_comments(request, page):
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        comments = Comment.objects.filter(approval=False)
        paginator = Paginator(comments, 10)
        try:
            comments = paginator.page(page)
        except PageNotAnInteger:
            comments = paginator.page(1)
        except EmptyPage:
            comments = paginator.page(paginator.num_pages)
    else:
        return redirect('home')

    context = {
        'comments': comments,
    }
    return render(request, 'dashboard/show_comments.html', context)


# Approve comment
@login_required
def approve_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        comment.approval = True
        comment.news.commentCount += 1
        comment.news.save()
        comment.save()
        return redirect('show-comments', page=1)
    else:
        return redirect('home')


# delete comment
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        comment.delete()
        return redirect('show-comments', page=1)
    else:
        return redirect('home')


# delete comment
@login_required
def delete_note(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        note.delete()
        return redirect('show-notes', page=1)
    else:
        return redirect('home')


# delete tag
@login_required
def delete_tag(request, pk):
    tag = get_object_or_404(Tag, pk=pk)
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        tag.delete()
        return redirect('show-tags', page=1)
    else:
        return redirect('home')


# delete tag
@login_required
def delete_user(request, pk):
    user1 = get_object_or_404(User, pk=pk)
    if request.user.type == 'chairman':
        user1.delete()
        return redirect('show-users', page=1)
    else:
        return redirect('home')


# Edit user
@login_required
def edit_user(request, pk):
    context = {}
    user1 = get_object_or_404(User, pk=pk)
    if request.user.type == 'chairman':
        context['user'] = user1
        if request.POST:
            user1.name = request.POST['name']
            user1.phone = request.POST['phone']
            user1.type = request.POST['type']

            user1.save()
            return redirect('show-users', page=1)
        else:
            return render(request, 'dashboard/edit_user.html', context)
    return redirect('home')


# Change user password
@login_required
def change_user_pass(request, pk):
    context = {}
    user1 = get_object_or_404(User, pk=pk)
    if request.user.type == 'chairman':
        context['user'] = user1
        if request.POST:
            user1.set_password(request.POST['password'])
            user1.save()
            return redirect('show-users', page=1)
        else:
            return render(request, 'dashboard/change_user_pass.html', context)
    return redirect('home')


# ِshow all news
@login_required
def show_all_news(request, page):
    news_list = News.objects.all()
    if request.GET.get('search'):
        news_list = News.objects.filter(title__icontains=request.GET.get('search'))
    if (request.user.type == 'chairman') or (request.user.type == 'editor_in_chief'):
        paginator = Paginator(news_list, 10)
        try:
            news_list = paginator.page(page)
        except PageNotAnInteger:
            news_list = paginator.page(1)
        except EmptyPage:
            news_list = paginator.page(paginator.num_pages)
        context = {
            'news_list': news_list,
        }
        return render(request, 'dashboard/show_all_news.html', context)

    return redirect('show-all-news', page=1)


# Add photo
@login_required
def add_photo(request):
    context = {}
    if request.user.type == 'chairman':
        form = PhotoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            Photo.objects.create(img=request.FILES['img'], title=request.POST['title'])
            return redirect('show-photos', page=1)
        context['form'] = form
        return render(request, 'dashboard/add_photo.html', context)
    else:
        return redirect('home')


# Edit photo
@login_required
def edit_photo(request, pk):
    context = {}
    photo = get_object_or_404(Photo, pk=pk)
    if request.user.type == 'chairman':
        context['photo'] = photo
        if request.POST:
            if 'img' in request.FILES:
                photo.img = request.FILES['img']
            photo.title = request.POST['title']
            photo.save()
            return redirect('show-photos', page=1)
        else:
            form = PhotoForm(instance=photo)
            context['form'] = form
        return render(request, 'dashboard/edit_photo.html', context)
    return redirect('home')


# Delete photo
@login_required
def delete_photo(request, pk):
    my_user = User.objects.get(id=request.user.id)
    if pk == 1 or pk == 2 or pk == 3 or pk == 4 or pk == 5:
        return redirect('home')
    photo = get_object_or_404(Photo, pk=pk)
    if my_user.type == 'chairman':
        photo.delete()
        return redirect('show-photos', page=1)
    else:
        return redirect('home')


# show all photo
@login_required
def show_photos(request, page):
    if request.user.type == 'chairman':
        photos = Photo.objects.all()
        paginator = Paginator(photos, 10)
        try:
            photos = paginator.page(page)
        except PageNotAnInteger:
            photos = paginator.page(1)
        except EmptyPage:
            photos = paginator.page(paginator.num_pages)
        context = {
            'photos': photos,
        }
        return render(request, 'dashboard/show_photos.html', context)
    else:
        return redirect('home')


# Add Advertising
@login_required
def add_advertising(request):
    context = {}
    if request.user.type == 'chairman':
        form = AdvertisingForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            Advertising.objects.create(img=request.FILES['img'], title=request.POST['title'])
            return redirect('show-all-advertising', page=1)
        context['form'] = form
        return render(request, 'dashboard/add_advertising.html', context)
    else:
        return redirect('home')


# Edit Advertising
@login_required
def edit_advertising(request, pk):
    context = {}
    advertising = get_object_or_404(Advertising, pk=pk)
    if request.user.type == 'chairman':
        context['advertising'] = advertising
        if request.POST:
            if 'img' in request.FILES:
                advertising.img = request.FILES['img']
            advertising.title = request.POST['title']
            advertising.save()
            return redirect('show-all-advertising', page=1)
        else:
            form = AdvertisingForm(instance=advertising)
            context['form'] = form
        return render(request, 'dashboard/edit_advertising.html', context)
    return redirect('home')


# Delete Advertising
@login_required
def delete_advertising(request, pk):
    my_user = User.objects.get(id=request.user.id)
    advertising = get_object_or_404(Advertising, pk=pk)
    if my_user.type == 'chairman':
        advertising.delete()
        return redirect('show-all-advertising', page=1)
    else:
        return redirect('home')


# show all Advertising
@login_required
def show_all_advertising(request, page):
    if request.user.type == 'chairman':
        advertisings = Advertising.objects.all()
        paginator = Paginator(advertisings, 10)
        try:
            advertisings = paginator.page(page)
        except PageNotAnInteger:
            advertisings = paginator.page(1)
        except EmptyPage:
            advertisings = paginator.page(paginator.num_pages)
        context = {
            'advertisings': advertisings,
        }
        return render(request, 'dashboard/show_all_advertisings.html', context)
    else:
        return redirect('home')


# Delete Subscriber
@login_required
def delete_subscriber(request, pk):
    subscriber = get_object_or_404(Subscriber, pk=pk)
    if request.user.type == 'chairman':
        subscriber.delete()
        return redirect('show-all-advertising', page=1)
    else:
        return redirect('home')


# show all subscribers
@login_required
def show_subscribers(request, page):
    if request.user.type == 'chairman':
        subscribers = Subscriber.objects.all()
        if request.GET.get('search'):
            subscribers = Subscriber.objects.filter(email__icontains=request.GET.get('search'))
        paginator = Paginator(subscribers, 10)
        try:
            subscribers = paginator.page(page)
        except PageNotAnInteger:
            subscribers = paginator.page(1)
        except EmptyPage:
            subscribers = paginator.page(paginator.num_pages)
        context = {
            'subscribers': subscribers,
        }
        return render(request, 'dashboard/show_subscribers.html', context)
    else:
        return redirect('home')


# Add subscriber
def postSubscriber(request):
    # request should be ajax and method should be POST.
    if request.is_ajax and request.method == "POST":
        if 'email' in request.POST:
            if (request.POST['email'] != "") and check(request.POST['email']):
                subscriber = Subscriber.objects.filter(email=request.POST['email']).count()
                if subscriber < 1:
                    Subscriber.objects.create(email=request.POST['email'])
                    return JsonResponse({"Subscriber": "done"}, status=200)
                else:
                    # some error occured
                    return JsonResponse({"error": "هذا البريد مشترك بالفعل"}, status=400)

    # some error occured
    return JsonResponse({"error": "من فضلك ادخل بريد الكترونى صحيح "}, status=400)


# Add tag to news
@login_required
def add_tag_to_news(request, tag_id, news_id):
    news = get_object_or_404(News, pk=news_id)
    cond = News.objects.filter(pk=news_id, user=request.user).count()
    tag = Tag.objects.filter(pk=tag_id).last()
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief' or cond > 0:
        if news and tag:
            Tag_news.objects.create(tag=tag, news=news)
    return redirect('news_details', pk=news_id)


# delete tag from news
@login_required
def delete_tag_from_news(request, tag_id, news_id):
    news = get_object_or_404(News, pk=news_id)
    cond = News.objects.filter(pk=news_id, user=request.user).count()
    tag = Tag.objects.filter(pk=tag_id).last()
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief' or cond > 0:
        if news and tag:
            Tag_news.objects.filter(tag=tag, news=news).last().delete()
    return redirect('news_details', pk=news_id)


@login_required
def tags_page(request, page, pk):
    cond = News.objects.filter(pk=pk, user=request.user).count()
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief' or cond > 0:
        tags = Tag.objects.all()
        if request.GET.get('search'):
            tags = Tag.objects.filter(text__icontains=request.GET.get('search'))
        paginator = Paginator(tags, 10)
        try:
            tags = paginator.page(page)
        except PageNotAnInteger:
            tags = paginator.page(1)
        except EmptyPage:
            tags = paginator.page(paginator.num_pages)
        news = News.objects.filter(pk=pk).last()
        context = {
            'tags': tags,
            'news': news,
        }
        return render(request, 'tags_page.html', context)
    return redirect('news_details', pk=pk)


# Add survey
@login_required
def add_survey(request):
    context = {}
    if request.user.type == 'editor_in_chief':
        form = SurveyForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            survey = Survey.objects.create(question=request.POST['question'], first_choice=request.POST['first_choice'],
                                           second_choice=request.POST['second_choice'])
            return redirect('show_surveys', page=1)
        context['form'] = form
        return render(request, 'dashboard/add_survey.html', context)
    else:
        return redirect('home')


@login_required
def show_surveys(request, page):
    if request.user.type == 'chairman' or request.user.type == 'editor_in_chief':
        surveys = Survey.objects.all()
        if request.GET.get('search'):
            surveys = Survey.objects.filter(question__icontains=request.GET.get('search'))
        paginator = Paginator(surveys, 10)
        try:
            surveys = paginator.page(page)
        except PageNotAnInteger:
            surveys = paginator.page(1)
        except EmptyPage:
            surveys = paginator.page(paginator.num_pages)
        context = {'surveys': surveys,
                   }
        return render(request, 'dashboard/show_surveys.html', context)
    else:
        return redirect('home')


# Edit survey
@login_required
def edit_survey(request, pk):
    context = {}
    survey = get_object_or_404(Survey, pk=pk)
    if request.user.type == 'chairman':
        context['survey'] = survey
        if request.POST:
            survey.question = request.POST['question']
            survey.first_choice = request.POST['first_choice']
            survey.second_choice = request.POST['second_choice']
            if 'approval' in request.POST:
                survey.approval = True
            else:
                survey.approval = False
            survey.save()
            return redirect('show-surveys', page=1)
        else:
            form = SurveyForm(instance=survey)
            context['form'] = form
        return render(request, 'dashboard/edit_survey.html', context)
    return redirect('home')


# Delete survey
@login_required
def delete_survey(request, pk):
    survey = get_object_or_404(Survey, pk=pk)
    if request.user.type == 'chairman':
        survey.delete()
        return redirect('show-surveys', page=1)
    else:
        return redirect('home')


# ِshow comments
@login_required
def show_categories(request, page):
    if request.user.type == 'chairman':
        categories = Category.objects.all()
        paginator = Paginator(categories, 10)
        try:
            categories = paginator.page(page)
        except PageNotAnInteger:
            categories = paginator.page(1)
        except EmptyPage:
            categories = paginator.page(paginator.num_pages)
    else:
        return redirect('home')

    context = {
        'categories': categories,
    }
    return render(request, 'dashboard/show_categories.html', context)


# Add photo
@login_required
def add_category(request):
    context = {}
    if request.user.type == 'chairman':
        form = CategoryForm(request.POST or None)
        print(request.POST)
        if form.is_valid():
            if request.POST['parent'] != "":
                parent = get_object_or_404(Category, pk=request.POST['parent'])
                Category.objects.create(name=request.POST['name'], parent=parent)
            else:
                Category.objects.create(name=request.POST['name'])
            return redirect('show-categories', page=1)
        context['form'] = form
        return render(request, 'dashboard/add_category.html', context)
    else:
        return redirect('home')


# Delete category
@login_required
def delete_category(request, pk):
    category = get_object_or_404(Category, pk=pk)
    if request.user.type == 'chairman':
        category.delete()
        return redirect('show-categories', page=1)
    else:
        return redirect('home')


# Edit category
@login_required
def edit_category(request, pk):
    context = {}
    category = get_object_or_404(Category, pk=pk)
    if request.user.type == 'chairman':
        context['category'] = category
        if request.POST:
            category.name = request.POST['name']
            if request.POST['parent'] != "":
                parent = get_object_or_404(Category, pk=request.POST['parent'])
                category.parent = parent
            else:
                category.parent = None
            category.save()
            return redirect('show-categories', page=1)
        else:
            form = CategoryForm(instance=category)
            context['form'] = form
        return render(request, 'dashboard/edit_category.html', context)
    return redirect('home')


# Add book
@login_required
def add_book(request):
    context = {}
    if request.user.type == 'editor_in_chief':
        form = BookForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            book = Book.objects.create(img=request.FILES['img'], title=request.POST['title'],
                                       user=request.user, details=request.POST['details'])
            return redirect('book_details', pk=book.pk)
        context['form'] = form
        return render(request, 'dashboard/add_book.html', context)
    else:
        return redirect('home')


# ِshow books
@login_required
def show_books(request, page):
    if request.user.type == 'chairman':
        books = Book.objects.all()
    else:
        return redirect('home')
    paginator = Paginator(books, 10)
    try:
        books = paginator.page(page)
    except PageNotAnInteger:
        books = paginator.page(1)
    except EmptyPage:
        books = paginator.page(paginator.num_pages)

    context = {
        'books': books,
    }
    return render(request, 'dashboard/show_books.html', context)


# delete book
@login_required
def delete_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.user.type == 'chairman':
        book.delete()
        return redirect('show-books', page=1)
    else:
        return redirect('home')


# Edit book
@login_required
def edit_book(request, pk):
    context = {}
    book = get_object_or_404(Book, pk=pk)
    if request.user.type == 'chairman':
        context['book'] = book
        if request.POST:
            if 'img' in request.FILES:
                book.img = request.FILES['img']
            book.title = request.POST['title']
            book.details = request.POST['details']
            book.save()
            return redirect('book_details', pk=pk)
        else:
            form = BookForm(instance=book)
            context['form'] = form
        return render(request, 'dashboard/edit_book.html', context)
    return redirect('book_details', pk=pk)


# ِshow videos
@login_required
def show_videos(request, page):
    if request.user.type == 'chairman':
        videos = Video.objects.all()
    else:
        return redirect('home')
    paginator = Paginator(videos, 10)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    context = {
        'videos': videos,
    }
    return render(request, 'dashboard/show_videos.html', context)


# Add Video
@login_required
def add_video(request):
    context = {}
    if request.user.type == 'chairman':
        form = VideoForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            video = Video.objects.create(title=request.POST['title'],
                                         link=request.POST['link'])
            return redirect('show-videos', page=1)
        context['form'] = form
        return render(request, 'dashboard/add_video.html', context)
    else:
        return redirect('home')


# Edit video
@login_required
def edit_video(request, pk):
    context = {}
    video = get_object_or_404(Video, pk=pk)
    if request.user.type == 'chairman':
        context['video'] = video
        if request.POST:
            video.title = request.POST['title']
            video.link = request.POST['link']
            video.save()
            return redirect('show-videos', page=1)
        else:
            form = VideoForm(instance=video)
            context['form'] = form
        return render(request, 'dashboard/edit_video.html', context)
    return redirect('show-videos', page=1)


# delete video
@login_required
def delete_video(request, pk):
    video = get_object_or_404(Video, pk=pk)
    if request.user.type == 'chairman':
        video.delete()
        return redirect('show-videos', page=1)
    else:
        return redirect('home')


# ِshow audios
@login_required
def show_audios(request, page):
    if request.user.type == 'chairman':
        videos = Audio.objects.all()
    else:
        return redirect('home')
    paginator = Paginator(videos, 10)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    context = {
        'videos': videos,
    }
    return render(request, 'dashboard/show_audios.html', context)


# Add audio
@login_required
def add_audio(request):
    context = {}
    if request.user.type == 'chairman':
        form = AudioForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            video = Audio.objects.create(title=request.POST['title'],
                                         link=request.POST['link'])
            return redirect('show-audios', page=1)
        context['form'] = form
        return render(request, 'dashboard/add_audio.html', context)
    else:
        return redirect('home')


# Edit audio
@login_required
def edit_audio(request, pk):
    context = {}
    video = get_object_or_404(Audio, pk=pk)
    if request.user.type == 'chairman':
        context['video'] = video
        if request.POST:
            video.title = request.POST['title']
            video.link = request.POST['link']
            video.save()
            return redirect('show-audios', page=1)
        else:
            form = AudioForm(instance=video)
            context['form'] = form
        return render(request, 'dashboard/edit_audio.html', context)
    return redirect('show-audios', page=1)


# delete audio
@login_required
def delete_audio(request, pk):
    audio = get_object_or_404(Audio, pk=pk)
    if request.user.type == 'chairman':
        audio.delete()
        return redirect('show-audios', page=1)
    else:
        return redirect('home')


# ِshow tvs
@login_required
def show_tvs(request, page):
    if request.user.type == 'chairman':
        videos = TV.objects.all()
    else:
        return redirect('home')
    paginator = Paginator(videos, 10)
    try:
        videos = paginator.page(page)
    except PageNotAnInteger:
        videos = paginator.page(1)
    except EmptyPage:
        videos = paginator.page(paginator.num_pages)

    context = {
        'videos': videos,
    }
    return render(request, 'dashboard/show_tvs.html', context)


# Add tv
@login_required
def add_tv(request):
    context = {}
    if request.user.type == 'chairman':
        form = TVForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            video = TV.objects.create(title=request.POST['title'],
                                      link=request.POST['link'])
            return redirect('show-tvs', page=1)
        context['form'] = form
        return render(request, 'dashboard/add_tv.html', context)
    else:
        return redirect('home')


# Edit tv
@login_required
def edit_tv(request, pk):
    context = {}
    video = get_object_or_404(TV, pk=pk)
    if request.user.type == 'chairman':
        context['video'] = video
        if request.POST:
            video.title = request.POST['title']
            video.link = request.POST['link']
            video.save()
            return redirect('show-tvs', page=1)
        else:
            form = TVForm(instance=video)
            context['form'] = form
        return render(request, 'dashboard/edit_tv.html', context)
    return redirect('show-tvs', page=1)


# delete tv
@login_required
def delete_tv(request, pk):
    audio = get_object_or_404(TV, pk=pk)
    if request.user.type == 'chairman':
        audio.delete()
        return redirect('show-tvs', page=1)
    else:
        return redirect('home')
