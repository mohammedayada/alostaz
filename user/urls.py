from django.urls import path
from .views import (
    user_login,
    user_logout,
    add_user,
    show_users,
    add_note,
    show_notes,
    add_tag,
    show_tags,
    add_news,
    show_news,
    show_all_news,
    approve_news,
    delete_news,
    edit_news,
    show_comments,
    approve_comment,
    delete_comment,
    delete_note,
    delete_tag,
    delete_user,
    edit_user,
    change_user_pass,
    add_photo,
    add_advertising,
    edit_photo,
    edit_advertising,
    show_photos,
    show_all_advertising,
    delete_photo,
    delete_advertising,
    delete_subscriber,
    show_subscribers,
    postSubscriber,

)

urlpatterns = [
    # login
    path('login', user_login, name='login'),
    # logout
    path('logout', user_logout, name='logout'),
    # add user
    path('add-user/', add_user, name='add-user'),
    # show users
    path('show-users/<int:page>/', show_users, name='show-users'),
    # delete user
    path('delete-user/<int:pk>', delete_user, name='delete-user'),
    # edit user
    path('edit-user/<int:pk>', edit_user, name='edit-user'),
    # change user password
    path('change-user-pass/<int:pk>', change_user_pass, name='change-user-pass'),
    # add note
    path('add-note/', add_note, name='add-note'),
    # delete note
    path('delete-note/<int:pk>', delete_note, name='delete-note'),
    # show notes
    path('show-notes/<int:page>/', show_notes, name='show-notes'),
    # add tag
    path('add-tag/', add_tag, name='add-tag'),
    # delete tag
    path('delete-tag/<int:pk>', delete_tag, name='delete-tag'),
    # show tags
    path('show-tags/<int:page>/', show_tags, name='show-tags'),
    # add news
    path('add-news/', add_news, name='add-news'),
    # show news
    path('show-news/<int:page>/', show_news, name='show-news'),
    # show all news
    path('show-all-news/<int:page>/', show_all_news, name='show-all-news'),
    # Approve news
    path('approve-news/<int:pk>', approve_news, name='approve-news'),
    # delete news
    path('delete-news/<int:pk>', delete_news, name='delete-news'),
    # edit news
    path('edit-news/<int:pk>', edit_news, name='edit-news'),
    # show comments
    path('show-comments/<int:page>/', show_comments, name='show-comments'),
    # Approve comment
    path('approve-comment/<int:pk>', approve_comment, name='approve-comment'),
    # delete comment
    path('delete-comment/<int:pk>', delete_comment, name='delete-comment'),
    # add advertising
    path('add-advertising/', add_advertising, name='add-advertising'),
    # show all advertising
    path('show-all-advertising/<int:page>/', show_all_advertising, name='show-all-advertising'),
    # edit advertising
    path('edit-advertising/<int:pk>', edit_advertising, name='edit-advertising'),
    # delete advertising
    path('delete-advertising/<int:pk>', delete_advertising, name='delete-advertising'),
    # show photos
    path('show-photos/<int:page>/', show_photos, name='show-photos'),
    # add photo
    path('add-photo/', add_photo, name='add-photo'),
    # edit photo
    path('edit-photo/<int:pk>', edit_photo, name='edit-photo'),
    # delete photo
    path('delete-photo/<int:pk>', delete_photo, name='delete-photo'),
    # show subscribers
    path('show-subscribers/<int:page>/', show_subscribers, name='show-subscribers'),
    # delete subscriber
    path('delete-subscriber/<int:pk>', delete_subscriber, name='delete-subscriber'),
    # Add Comment by using AJAX
    path('post/ajax/Subscriber/', postSubscriber, name='post-subscriber'),

]
