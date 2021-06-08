from . import views

from django.urls import path

from django.conf.urls import url

app_name = 'posts'

urlpatterns = [
    path('create_post', views.create_post, name='create_post'),
    path('delete_post/(?P<post_id>[0-9]+)', views.delete_post, name='delete_post'),
    url(r'^ajax/like_or_delete_like_post$', views.like_or_delete_like_post, name='like_or_delete_like_post'),
    path('post/<int:post_id>', views.post, name='post')
]