from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login , authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from . forms import PostForm
from . models import Post, Category, Tag
#import paginator and JsonResponse
from django.core.paginator import Paginator
from django.http import JsonResponse
#import pop edit
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse


def home(request):
    posts = Post.objects.all().order_by('-date_created')
    return render(request, 'blog/index.html', {'posts': posts})



def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('home')
    return render(request, 'blog/register.html')


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'invalid credential')
            return redirect('login')
    return render(request, 'blog/login.html')

def logout_view(request):
    logout(request)
    return redirect('login')



@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)  # Don't save yet
            post.author = request.user      # Set the logged-in user as author
            post.save()                     # Now save
            form.save_m2m()  # Save many-to-many data (tags)
            return redirect('home')
    else:
        #print(form.errors)  # Add this line for debugging
        form = PostForm()
    return render(request, 'blog/create_post.html', {'form': form})


def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')  # After deletion, go to index page
    return render(request, 'blog/delete_post.html', {'post': post})



def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    posts = Post.objects.filter(category=category)
    return render(request, 'blog/posts_by_category.html', {'category': category, 'posts': posts})

def posts_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    posts = Post.objects.filter(tags=tag)
    return render(request, 'blog/posts_by_tag.html', {'tag': tag, 'posts': posts})

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, 'blog/post_detail.html', {'post': post})

def index(request):
    post_list = Post.objects.all().order_by('-date_created')
    paginator = Paginator(post_list, 5)  # 5 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    return render(request, 'index.html', {'posts': posts})

def ajax_delete_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, id=post_id)
        if post.author == request.user:
            post.delete()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'forbidden'})
    return JsonResponse({'status': 'error'})

@csrf_exempt
def ajax_edit_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        title = request.POST.get('title')
        content = request.POST.get('content')

        post = get_object_or_404(Post, id=post_id)
        if post.author == request.user:
            post.title = title
            post.content = content
            post.save()
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'status': 'forbidden'})
    return JsonResponse({'status': 'error'})




