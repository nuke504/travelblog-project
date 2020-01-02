from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from .models import Blogger
from blogs.models import Blog, Vote

def login(request):
    if request.method == 'POST':
        user = auth.authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            auth.login(request, user)
            try:
                blogger = Blogger.objects.get(user = user)
                return redirect('home')
            except:
                return render(request, 'accounts/change_password.html', {'error':'As this is your first time logging in, you need to update your profile.'})
        else:
            return render(request, 'accounts/login.html', {'error':'Username or password is invalid.'})
    else:
        return render(request, 'accounts/login.html')

@login_required
def change_password(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            try:
                validate_password(request.POST['password1'], user=request.user)
            except ValidationError:
                return render(request, 'accounts/change_password.html', {'error':'Your password does not meet minimum requirements'})
            user = request.user
            user.set_password(request.POST['password1'])
            user.save()
            auth.login(request, user)
            try:
                blogger = Blogger.objects.get(user = user)
            except:
                blogger = Blogger()
            blogger.user = request.user
            blogger.timeFirstModification = timezone.datetime.now()
            blogger.description = request.POST['description']
            blogger.displayName = request.POST['displayName']
            if request.FILES.get('image',False): # Upload images if there are
                blogger.profilepic = request.FILES['image']
            blogger.save()
            return redirect('home')
        else:
            return render(request, 'accounts/change_password.html', {'error':'Passwords do not match'})
    else:
        return render(request, 'accounts/change_password.html')

def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('home')

def profile(request, blogger_id):
    blogger = get_object_or_404(Blogger, pk = blogger_id)
    blogs = Blog.objects.filter(blogger = blogger)
    totalVotes = len(Vote.objects.filter(blogger = blogger))
    totalBlogs = len(blogs)
    return render(request, 'accounts/profile.html', {'blogger':blogger,'blogs':blogs,'totalVotes':totalVotes,'totalBlogs':totalBlogs})