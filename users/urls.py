from . import views

from django.urls import path, include

from django.conf.urls import url


app_name = 'users'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
    path('main/', views.main, name='main'),
    path('logout/', views.logout, name='logout'),
    path('profile/<int:user_id>', views.profile, name='profile'),
    path('settings/', views.settings, name='settings'),
    path('photo_album/<int:user_id>', views.photo_album, name='photo_album'),
    path('add_photo', views.add_photo, name='add_photo'),
    path('users', views.FindUsers.as_view(), name='users'),
    path('activate_user/<uidb64>/<token>', views.activate_user, name='activate'),
    url(r'^ajax/change_avatar/$', views.change_avatar, name='change_avatar'),
    # path('find_users', views.FindUsers, name='find_users'),
    # path('photo/<int:user_id>_<int:photo_id>', views.photo, name='photo')
 ]
