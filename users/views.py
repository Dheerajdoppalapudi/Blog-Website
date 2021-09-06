from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import login_required
from blog.models import Post
from .models import User
from django.http import Http404


# Create your views here.
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created. You can now login')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request, username):
    # current_user = request.user
    try:
        current_user_id = User.objects.get(username=username)
    except User.DoesNotExist:
        raise Http404("User Does Not Exist")
    profile_context = {
        "user_posts": Post.objects.filter(author=current_user_id),
        "queried_user": User.objects.get(username=username)
    }
    return render(request, 'users/profile.html', profile_context)

@login_required
def specific_blog(request, username, title):
    try:
        current_user_id = User.objects.get(username=username)
        post = Post.objects.get(title=title, author=current_user_id)
    except User.DoesNotExist:
        raise Http404("User Does Not Exist")
    context = {
            "user_post": post
        }
    return render(request, 'users/userblog.html', context)