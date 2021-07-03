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
    add_tag_to_news,
    tags_page,
    delete_tag_from_news,
    show_surveys,
    add_survey,
    edit_survey,
    delete_survey,
    show_categories,
    add_category,
    delete_category,
    edit_category,
    add_book,
    show_books,
    edit_book,
    delete_book,



)

urlpatterns = [
    # login
    path('login', user_login, name='login'),
    # logout
    path('logout', user_logout, name='logout'),
    # user ----------------------------------------------------
    # add user
    path('add-user/', add_user, name='add-user'),
    # show users
    path('show-users/<int:page>', show_users, name='show-users'),
    # delete user
    path('delete-user/<int:pk>', delete_user, name='delete-user'),
    # edit user
    path('edit-user/<int:pk>', edit_user, name='edit-user'),
    # change user password
    path('change-user-pass/<int:pk>', change_user_pass, name='change-user-pass'),
    # note -------------------------------------------------------
    # add note
    path('add-note/', add_note, name='add-note'),
    # delete note
    path('delete-note/<int:pk>', delete_note, name='delete-note'),
    # show notes
    path('show-notes/<int:page>', show_notes, name='show-notes'),
    # tag -------------------------------------------------------
    # add tag
    path('add-tag/', add_tag, name='add-tag'),
    # delete tag
    path('delete-tag/<int:pk>', delete_tag, name='delete-tag'),
    # show tags
    path('show-tags/<int:page>', show_tags, name='show-tags'),
    # tag page
    path('tags-page/<int:page>/<int:pk>', tags_page, name='tags-page'),
    # Add tag to news
    path('add-tag-to-news/<int:news_id>/<int:tag_id>/', add_tag_to_news, name='add-tag-to-news'),
    # delete tag from news
    path('delete-tag-from-news/<int:news_id>/<int:tag_id>/', delete_tag_from_news, name='delete-tag-from-news'),
    # news --------------------------------------------------------
    # add news
    path('add-news/', add_news, name='add-news'),
    # show news
    path('show-news/<int:page>', show_news, name='show-news'),
    # show all news
    path('show-all-news/<int:page>', show_all_news, name='show-all-news'),
    # Approve news
    path('approve-news/<int:pk>', approve_news, name='approve-news'),
    # delete news
    path('delete-news/<int:pk>', delete_news, name='delete-news'),
    # edit news
    path('edit-news/<int:pk>', edit_news, name='edit-news'),
    # comment ------------------------------------------------------
    # show comments
    path('show-comments/<int:page>', show_comments, name='show-comments'),
    # Approve comment
    path('approve-comment/<int:pk>', approve_comment, name='approve-comment'),
    # delete comment
    path('delete-comment/<int:pk>', delete_comment, name='delete-comment'),
    # Add Comment by using AJAX
    path('post/ajax/Subscriber/', postSubscriber, name='post-subscriber'),
    # advertising -------------------------------------------------------
    # add advertising
    path('add-advertising/', add_advertising, name='add-advertising'),
    # show all advertising
    path('show-all-advertising/<int:page>', show_all_advertising, name='show-all-advertising'),
    # edit advertising
    path('edit-advertising/<int:pk>', edit_advertising, name='edit-advertising'),
    # delete advertising
    path('delete-advertising/<int:pk>', delete_advertising, name='delete-advertising'),
    # photo ----------------------------------------------------------------
    # show photos
    path('show-photos/<int:page>', show_photos, name='show-photos'),
    # add photo
    path('add-photo/', add_photo, name='add-photo'),
    # edit photo
    path('edit-photo/<int:pk>', edit_photo, name='edit-photo'),
    # delete photo
    path('delete-photo/<int:pk>', delete_photo, name='delete-photo'),
    # subscribers ----------------------------------------------------------
    # show subscribers
    path('show-subscribers/<int:page>', show_subscribers, name='show-subscribers'),
    # delete subscriber
    path('delete-subscriber/<int:pk>', delete_subscriber, name='delete-subscriber'),
    # surveys -------------------------------------------------------------
    # show surveys
    path('show-surveys/<int:page>', show_surveys, name='show-surveys'),
    # add survey
    path('add-survey/', add_survey, name='add-survey'),
    # edit survey
    path('edit-survey/<int:pk>', edit_survey, name='edit-survey'),
    # delete survey
    path('delete-survey/<int:pk>', delete_survey, name='delete-survey'),
    # ------------------------------------------------الأقسام categories
    # show categories
    path('show-categories/<int:page>', show_categories, name='show-categories'),
    # add survey
    path('add-category/', add_category, name='add-category'),
    # delete category
    path('delete-category/<int:pk>', delete_category, name='delete-category'),
    # edit category
    path('edit-category/<int:pk>', edit_category, name='edit-category'),
    # الكتب books ------------------------------------------------------
    # add book
    path('add-book/', add_book, name='add-book'),
    # show books
    path('show-books/<int:page>', show_books, name='show-books'),
    # edit book
    path('edit-book/<int:pk>', edit_book, name='edit-book'),
    # delete book
    path('delete-book/<int:pk>', delete_book, name='delete-book'),

]
