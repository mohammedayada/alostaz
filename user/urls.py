from django.urls import path
from .views import (
    user_login,
    user_logout,
    dashboard,
    add_user,
    show_users,
    add_note,
    show_notes

)

urlpatterns = [
    # login
    path('login', user_login, name='login'),
    # logout
    path('logout', user_logout, name='logout'),
    # main dashboard
    path('', dashboard, name='main-dashboard'),
    # add user
    path('add-user/', add_user, name='add-user'),
    # show users
    path('show-users/', show_users, name='show-users'),
    # add note
    path('add-note/', add_note, name='add-note'),
    # show notes
    path('show-notes/', show_notes, name='show-notes'),

]
