from django.urls import path
from .views import (
    user_login,
    user_logout,
    dashboard,
    add_user,
    show_users,
    add_note,
    show_notes,
    add_tag,
    show_tags,
    add_news,
    show_news,
    approve_news,
    delete_news,
    edit_news,
    show_comments,
    approve_comment,
    delete_comment,
    delete_note,
    delete_tag,

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
    # delete note
    path('delete-note/<int:pk>', delete_note, name='delete-note'),
    # show notes
    path('show-notes/', show_notes, name='show-notes'),
    # add tag
    path('add-tag/', add_tag, name='add-tag'),
    # delete note
    path('delete-tag/<int:pk>', delete_tag, name='delete-tag'),
    # show tags
    path('show-tags/', show_tags, name='show-tags'),
    # add tag
    path('add-news/', add_news, name='add-news'),
    # show news
    path('show-news/', show_news, name='show-news'),
    # Approve news
    path('approve-news/<int:pk>', approve_news, name='approve-news'),
    # delete news
    path('delete-news/<int:pk>', delete_news, name='delete-news'),
    # edit news
    path('edit-news/<int:pk>', edit_news, name='edit-news'),
    # show comments
    path('show-comments/', show_comments, name='show-comments'),
    # Approve comment
    path('approve-comment/<int:pk>', approve_comment, name='approve-comment'),
    # delete comment
    path('delete-comment/<int:pk>', delete_comment, name='delete-comment'),

]
