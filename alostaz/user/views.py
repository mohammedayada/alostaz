from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import user, Photo, Advertising, Subscriber, Survey
from news.models import Note, Tag, News, Category, Comment, Tag_news, Book
from .forms import NewsForm, PhotoForm, AdvertisingForm, SurveyForm, CategoryForm, BookForm
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
        username = User.objects.filter(email=email).last().username
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman':
        msg = 'من فضلك ادخل بيانات صحيحه'
        if request.POST:
            if request.POST['email'] != "" and request.POST['name'] != "" and request.POST['password'] != "" and \
                    request.POST['type'] != "" and request.POST['phone'] != "":
                if user.objects.filter(email=request.POST['email']).count() == 0:
                    user.objects.create_user(
                        name=request.POST['name'],
                        email=request.POST['email'],
                        username=request.POST['email'],
                        phone=request.POST['phone'],
                        type=request.POST['type'],
                        password=request.POST['password'],
                        is_active=True,
                    )
                    return redirect('show-users', page=1)
                else:
                    msg = 'من فضلك ادخل بريد الكترونى صحيح'
        context = {'msg': msg,
                   'is_chairman': is_chairman,
                   'is_chef': is_chef,
                   }
        return render(request, 'dashboard/add_user.html', context)
    else:
        return redirect('home')


# Show user
@login_required
def show_users(request, page):
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman':
        users = user.objects.all()
        if request.GET.get('search'):
            users = user.objects.filter(name__icontains=request.GET.get('search'))
        paginator = Paginator(users, 10)
        try:
            users = paginator.page(page)
        except PageNotAnInteger:
            users = paginator.page(1)
        except EmptyPage:
            users = paginator.page(paginator.num_pages)
        context = {'users': users,
                   'is_chairman': is_chairman,
                   'is_chef': is_chef,
                   }
        return render(request, 'dashboard/show_users.html', context)
    else:
        return redirect('home')


@login_required
def add_note(request):
    # when request POST
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
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
                   'is_chairman': is_chairman,
                   'is_chef': is_chef
                   }
        return render(request, 'dashboard/add_note.html', context)
    else:
        return redirect('home')


# Show user
@login_required
def show_notes(request, page):
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        notes = Note.objects.all()
        paginator = Paginator(notes, 10)
        try:
            notes = paginator.page(page)
        except PageNotAnInteger:
            notes = paginator.page(1)
        except EmptyPage:
            notes = paginator.page(paginator.num_pages)
        context = {'notes': notes,
                   'is_chairman': is_chairman,
                   'is_chef': is_chef,
                   }
        return render(request, 'dashboard/show_notes.html', context)
    else:
        return redirect('home')


@login_required
def add_tag(request):
    # when request POST
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
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
                   'is_chairman': is_chairman,
                   'is_chef': is_chef,
                   }
        return render(request, 'dashboard/add_tag.html', context)
    else:
        return redirect('home')


# Show tags
@login_required
def show_tags(request, page):
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
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
                   'is_chairman': is_chairman,
                   'is_chef': is_chef,
                   }
        return render(request, 'dashboard/show_tags.html', context)
    else:
        return redirect('home')


# Add news
@login_required
def add_news(request):
    context = {}
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    cond = True
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        news_list = News.objects.filter(approval=False)
    elif my_user.type == 'editor':
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
        'is_chairman': is_chairman,
        'is_chef': is_chef,
    }
    return render(request, 'dashboard/show_news.html', context)


# Approve news
@login_required
def approve_news(request, pk):
    my_user = user.objects.get(id=request.user.id)
    news = get_object_or_404(News, pk=pk)
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        news.approval = True
        news.save()
        return redirect('news_details', pk=pk)
    elif my_user.type == 'editor':
        news = News.objects.filter(approval=False, user=request.user).last()
        news.approval = True
        news.save()
        return redirect('news_details', pk=pk)
    else:
        return redirect('home')


# delete news
@login_required
def delete_news(request, pk):
    my_user = user.objects.get(id=request.user.id)
    news = get_object_or_404(News, pk=pk)
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        news.delete()
        return redirect('show-news', page=1)
    elif my_user.type == 'editor':
        news = News.objects.filter(approval=False, user=request.user).last()
        news.delete()
        return redirect('show-news', page=1)
    else:
        return redirect('home')


# Edit news
@login_required
def edit_news(request, pk):
    context = {}
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    news = get_object_or_404(News, pk=pk)
    cond = News.objects.filter(pk=pk, user=request.user).count()
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief' or cond > 0:
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
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
        'is_chairman': is_chairman,
        'is_chef': is_chef,
    }
    return render(request, 'dashboard/show_comments.html', context)


# Approve comment
@login_required
def approve_comment(request, pk):
    my_user = user.objects.get(id=request.user.id)
    comment = get_object_or_404(Comment, pk=pk)
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
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
    my_user = user.objects.get(id=request.user.id)
    comment = get_object_or_404(Comment, pk=pk)
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        comment.delete()
        return redirect('show-comments', page=1)
    else:
        return redirect('home')


# delete comment
@login_required
def delete_note(request, pk):
    my_user = user.objects.get(id=request.user.id)
    note = get_object_or_404(Note, pk=pk)
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        note.delete()
        return redirect('show-notes', page=1)
    else:
        return redirect('home')


# delete tag
@login_required
def delete_tag(request, pk):
    my_user = user.objects.get(id=request.user.id)
    tag = get_object_or_404(Tag, pk=pk)
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        tag.delete()
        return redirect('show-tags', page=1)
    else:
        return redirect('home')


# delete tag
@login_required
def delete_user(request, pk):
    my_user = user.objects.get(id=request.user.id)
    user1 = get_object_or_404(user, pk=pk)
    if my_user.type == 'chairman':
        user1.delete()
        return redirect('show-users', page=1)
    else:
        return redirect('home')


# Edit user
@login_required
def edit_user(request, pk):
    context = {}
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    user1 = get_object_or_404(user, pk=pk)
    if my_user.type == 'chairman':
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    user1 = get_object_or_404(user, pk=pk)
    if my_user.type == 'chairman':
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if is_chef or is_chairman:
        paginator = Paginator(news_list, 10)
        try:
            news_list = paginator.page(page)
        except PageNotAnInteger:
            news_list = paginator.page(1)
        except EmptyPage:
            news_list = paginator.page(paginator.num_pages)
        context = {
            'news_list': news_list,
            'is_chairman': is_chairman,
            'is_chef': is_chef,
        }
        return render(request, 'dashboard/show_all_news.html', context)

    return redirect('show-all-news', page=1)


# Add photo
@login_required
def add_photo(request):
    context = {}
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    if my_user.type == 'chairman':
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    photo = get_object_or_404(Photo, pk=pk)
    if my_user.type == 'chairman':
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
    my_user = user.objects.get(id=request.user.id)
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman':
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
            'is_chairman': is_chairman,
            'is_chef': is_chef,
        }
        return render(request, 'dashboard/show_photos.html', context)
    else:
        return redirect('home')


# Add Advertising
@login_required
def add_advertising(request):
    context = {}
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    if my_user.type == 'chairman':
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    advertising = get_object_or_404(Advertising, pk=pk)
    if my_user.type == 'chairman':
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
    my_user = user.objects.get(id=request.user.id)
    advertising = get_object_or_404(Advertising, pk=pk)
    if my_user.type == 'chairman':
        advertising.delete()
        return redirect('show-all-advertising', page=1)
    else:
        return redirect('home')


# show all Advertising
@login_required
def show_all_advertising(request, page):
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman':
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
            'is_chairman': is_chairman,
            'is_chef': is_chef,
        }
        return render(request, 'dashboard/show_all_advertisings.html', context)
    else:
        return redirect('home')


# Delete Subscriber
@login_required
def delete_subscriber(request, pk):
    my_user = user.objects.get(id=request.user.id)
    subscriber = get_object_or_404(Subscriber, pk=pk)
    if my_user.type == 'chairman':
        subscriber.delete()
        return redirect('show-all-advertising', page=1)
    else:
        return redirect('home')


# show all subscribers
@login_required
def show_subscribers(request, page):
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman':
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
            'is_chairman': is_chairman,
            'is_chef': is_chef,
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
    my_user = user.objects.get(id=request.user.id)
    news = get_object_or_404(News, pk=news_id)
    cond = News.objects.filter(pk=news_id, user=request.user).count()
    tag = Tag.objects.filter(pk=tag_id).last()
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief' or cond > 0:
        if news and tag:
            Tag_news.objects.create(tag=tag, news=news)
    return redirect('news_details', pk=news_id)


# delete tag from news
@login_required
def delete_tag_from_news(request, tag_id, news_id):
    my_user = user.objects.get(id=request.user.id)
    news = get_object_or_404(News, pk=news_id)
    cond = News.objects.filter(pk=news_id, user=request.user).count()
    tag = Tag.objects.filter(pk=tag_id).last()
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief' or cond > 0:
        if news and tag:
            Tag_news.objects.filter(tag=tag, news=news).last().delete()
    return redirect('news_details', pk=news_id)


@login_required
def tags_page(request, page, pk):
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    cond = News.objects.filter(pk=pk, user=request.user).count()
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief' or cond > 0:
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
            'is_chairman': is_chairman,
            'is_chef': is_chef,
            'tags': tags,
            'news': news,
        }
        return render(request, 'tags_page.html', context)
    return redirect('news_details', pk=pk)


# Add survey
@login_required
def add_survey(request):
    context = {}
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    if is_chairman:
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
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
                   'is_chairman': is_chairman,
                   'is_chef': is_chef,
                   }
        return render(request, 'dashboard/show_surveys.html', context)
    else:
        return redirect('home')


# Edit survey
@login_required
def edit_survey(request, pk):
    context = {}
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    survey = get_object_or_404(Survey, pk=pk)
    if my_user.type == 'chairman':
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
    my_user = user.objects.get(id=request.user.id)
    survey = get_object_or_404(Survey, pk=pk)
    if my_user.type == 'chairman':
        survey.delete()
        return redirect('show-surveys', page=1)
    else:
        return redirect('home')


# ِshow comments
@login_required
def show_categories(request, page):
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman':
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
        'is_chairman': is_chairman,
        'is_chef': is_chef,
    }
    return render(request, 'dashboard/show_categories.html', context)


# Add photo
@login_required
def add_category(request):
    context = {}
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    if my_user.type == 'chairman':
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
    my_user = user.objects.get(id=request.user.id)
    category = get_object_or_404(Category, pk=pk)
    if my_user.type == 'chairman':
        category.delete()
        return redirect('show-categories', page=1)
    else:
        return redirect('home')


# Edit category
@login_required
def edit_category(request, pk):
    context = {}
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    category = get_object_or_404(Category, pk=pk)
    if my_user.type == 'chairman':
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    if is_chairman:
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
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    if my_user.type == 'chairman':
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
        'is_chairman': is_chairman,
        'is_chef': is_chef,
    }
    return render(request, 'dashboard/show_books.html', context)

# delete book
@login_required
def delete_book(request, pk):
    my_user = user.objects.get(id=request.user.id)
    book = get_object_or_404(Book, pk=pk)
    if my_user.type == 'chairman':
        book.delete()
        return redirect('show-books', page=1)
    else:
        return redirect('home')


# Edit book
@login_required
def edit_book(request, pk):
    context = {}
    my_user = user.objects.get(id=request.user.id)
    is_chairman = (my_user.type == 'chairman')
    is_chef = (my_user.type == 'editor_in_chief')
    context['is_chairman'] = is_chairman
    context['is_chef'] = is_chef
    book = get_object_or_404(Book, pk=pk)
    if my_user.type == 'chairman':
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