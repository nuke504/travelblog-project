import numpy as np

from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from accounts.models import Blogger
from .models import Blog, Vote

# Create your views here.
def home(request):
    allBlogs = Blog.objects.all()
    bannerBlogs = Blog.objects.filter(banner = True)
    if len(allBlogs) > 3:
        allBlogs = allBlogs.order_by('-id')[0:3]
    if len(bannerBlogs) > 3:
        bannerBlogs = np.random.choice(bannerBlogs, 3, replace = False)
    return render(request, 'blogs/home.html', {'bloggers':Blogger.objects,'blogsList':allBlogs, 'bannerBlogs':bannerBlogs})

@login_required
def create(request):
    if request.method == 'POST':
        blog = Blog()
        blog.title = request.POST['title']
        blog.pub_date = timezone.datetime.now()
        blog.image = request.FILES['image']
        blog.body = request.POST['body']
        blog.blogger = Blogger.objects.get(user = request.user)
        if request.POST['banner'] == 'True':
            blog.banner = True
        blog.save()
        return redirect('home')
    else:
        return render(request, 'blogs/create_blog.html')

def detail(request, blog_id):
    blog = get_object_or_404(Blog, pk = blog_id)
    return render(request, 'blogs/detail.html', {'blog':blog})

def upvote(request, blog_id):
    if request.method == 'POST': # Ensure that it is a post request
        blog = get_object_or_404(Blog, pk = blog_id)
        if not request.user.is_authenticated:
            return render(request, 'blogs/detail.html',{'blog':blog,'error':'You need to be logged in to like a post'})
        else:
            try:
                vote = Vote.objects.get(blog = blog, blogger=Blogger.objects.get(user = request.user))
                return render(request, 'blogs/detail.html',{'blog':blog,'error':'You have already voted'})
            except Vote.DoesNotExist:
                vote = Vote()
                vote.blogger = Blogger.objects.get(user = request.user)
                vote.blog = blog
                vote.vote_date = timezone.datetime.now()
                vote.save()
                return render(request, 'blogs/detail.html', {'blog':blog})

@login_required
def delete(request, blog_id):
    if request.method == 'POST': # Ensure that it is a post request
        blog = get_object_or_404(Blog, pk = blog_id)
        if not request.user.is_authenticated:
            return render(request, 'blogs/detail.html',{'blog':blog,'error':'You need to be logged in to delete a post'})
        else:
            blog.delete()
            bloggerID = Blogger.objects.get(user = request.user).id
            return redirect('profile',bloggerID)