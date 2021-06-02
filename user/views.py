from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import user
from news.models import Note, Tag, News, Category, Comment
from .forms import NewsForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
            if request.POST['email'] != "" and request.POST['name'] != "" and request.POST['password'] != "" and request.POST['type'] != "" and request.POST['phone'] != "":
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
    news = News.objects.filter(pk=pk).last()
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
    news = News.objects.filter(pk=pk).last()
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
    news = News.objects.get(pk=pk)
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
    comment = Comment.objects.filter(pk=pk).last()
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        comment.approval = True
        comment.save()
        return redirect('show-comments', page=1)
    else:
        return redirect('home')


# delete comment
@login_required
def delete_comment(request, pk):
    my_user = user.objects.get(id=request.user.id)
    comment = Comment.objects.filter(pk=pk).last()
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        comment.delete()
        return redirect('show-comments', page=1)
    else:
        return redirect('home')


# delete comment
@login_required
def delete_note(request, pk):
    my_user = user.objects.get(id=request.user.id)
    note = Note.objects.filter(pk=pk).last()
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        note.delete()
        return redirect('show-notes', page=1)
    else:
        return redirect('home')


# delete tag
@login_required
def delete_tag(request, pk):
    my_user = user.objects.get(id=request.user.id)
    tag = Tag.objects.filter(pk=pk).last()
    if my_user.type == 'chairman' or my_user.type == 'editor_in_chief':
        tag.delete()
        return redirect('show-tags', page=1)
    else:
        return redirect('home')
