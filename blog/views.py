from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import Post
from users.models import User

@login_required
def home(request):
    context = {
        'posts' : Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})

@login_required
def search_name(request):
    if request.method == "POST":
        form_data = request.POST.get('title')
        try:
            current_user = User.objects.get(username=form_data)
            post = Post.objects.filter(author=current_user)
            context = {
                "user_posts": post,
                "queried_user": form_data
            }
            return render(request, 'blog/search.html', context)
        except User.DoesNotExist:
            try:
                post = Post.objects.filter(title__contains=form_data)
                context = {
                    "user_posts": post,
                    "queried_user": form_data
                }
                return render(request, 'blog/search.html', context)
            except Post.DoesNotExist:
                pass
        context = {
            "queried_user": form_data,
            "message": "nothing matched your search result",
        }
        return render(request, 'blog/search.html', context)