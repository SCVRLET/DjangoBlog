from django.shortcuts import render, redirect

from users.models import Post, User, Like

from django.utils import timezone

from django.http import JsonResponse

from django.views.decorators.csrf import csrf_exempt
# Create your views here.

def create_post(request):
    if request.method == "POST":
        post_text = str(request.POST['autoresizing'])
        current_user = User.objects.filter(id=request.user.id).first()

        new_post = Post.objects.create(text=post_text, created_at=timezone.localtime(timezone.now()), 
        user_id=current_user)

        return redirect('users:profile', user_id=request.user.id)

def delete_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.filter(id=post_id).first()
        post.delete()

        return redirect('users:profile', user_id=request.user.id)


@csrf_exempt
def like_or_delete_like_post(request):
    if request.is_ajax() and request.method == "POST":
        post_id = int(request.POST['d[0][value]'])
        curr_user =  User.objects.filter(id=request.user.id).first()
        curr_post = Post.objects.filter(id=post_id).first()
        data = {'like': True }

        if Like.objects.filter(user=curr_user).exists():
            Like.objects.filter(post=curr_post, user=curr_user).delete()
            curr_post.liked.remove(curr_user)

            data['like'] = False
    
        else:
            like = Like.objects.create(user=curr_user, post=curr_post)
            curr_post.liked.add(curr_user)

            like.save()
        
        data['likes_number'] = Post.objects.filter(id=post_id).first().total_likes

        return JsonResponse(data)


def post(request, post_id):
    try:
        post = Post.objects.filter(id=post_id).first()
        context = {'post': post}

        return render(request, 'main/post.html', context)
    
    except:
        return render(request, 'errors/post_not_found.html')