from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import user
from news.models import Note

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
            return redirect('main-dashboard')

    return redirect('home')


# logout function
@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    return render(request, 'dashboard/main.html')

# add user
@login_required
def add_user(request):
    # when request POST
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
                return redirect('show-users')
            else:
                msg = 'من فضلك ادخل بريد الكترونى صحيح'
    context = {'msg': msg}
    return render(request, 'dashboard/add_user.html', context)
# Show user
@login_required
def show_users(request):
    users = user.objects.all()
    context = {'users': users}
    return render(request, 'dashboard/show_users.html', context)
@login_required
def add_note(request):
    # when request POST
    msg = 'من فضلك ادخل بيانات صحيحه'
    if request.POST:
        if request.POST['title'] != "" and request.POST['link'] != "" :
                Note.objects.create(
                    user=request.user,
                    title=request.POST['title'],
                    link=request.POST['link'],
                )
                return redirect('show-notes')
    context = {'msg': msg}
    return render(request, 'dashboard/add_note.html', context)

# Show user
@login_required
def show_notes(request):
    notes = Note.objects.all()
    context = {'notes': notes}
    return render(request, 'dashboard/show_notes.html', context)