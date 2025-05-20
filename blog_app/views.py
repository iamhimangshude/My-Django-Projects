from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.views.generic.base import View
# from django.http import HttpResponse

from auth_app.models import UserModel
from blog_app.forms import AddBlogPost
from blog_app.models import Post

# Create your views here.

def index(request):
    return render(request, 'blog_app/index.html')

def all_blogs(request):
    request.session['off_home'] = False
    all_posts = Post.objects.all()[::-1]
    if not request.user.is_authenticated:
        all_posts_for_not_authenticated = all_posts[:3]
        return render(request, 'blog_app/all_blogs.html', {'all_posts':all_posts_for_not_authenticated})
        
    
        
    # return HttpResponse("Hello World",)
    return render(request, 'blog_app/all_blogs.html', {'all_posts':all_posts})


def blog_detail_view(request, id):
    post = Post.objects.get(post_id=id)
    request.session['off_home'] = True

    return render(request, 'blog_app/blog_detail.html', {'post':post,},)


@login_required
def create_blog(request):
    form = AddBlogPost()
    if request.method == 'POST':
        form = AddBlogPost(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.creator = request.user
            post.save()
            return redirect('all-blogs')
        
        return render(request, "blog_app/add_blog_post.html", {'form':form, 'title':'Create', 'btnTitle':'Create'})
        
    return render(request, "blog_app/add_blog_post.html", {'form':form, 'title':'Create', 'btnTitle':'Create'})


@login_required
def list_user_blogs(request):
    user = request.user
    request.session['off_home']=True
    user_blog_posts = Post.objects.filter(creator=user)
    return render(request, 'blog_app/user_blogs.html', {'blogs':user_blog_posts})
    

class EditBlogView(View):
    def get(self, request, id):
        post_data = Post.objects.get(post_id=id)
        edit_form = AddBlogPost(instance=post_data)
        return render(request, 'blog_app/add_blog_post.html', {'form':edit_form, 'title':"Update", 'btnTitle':"Update"})

    def post(self, request, id):
        post_data = Post.objects.get(post_id=id)
        edit_form = AddBlogPost(request.POST, instance=post_data)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('user-blogs')
        return render(request, 'blog_app/add_blog_post.html', {'form':edit_form, 'title':"Update", 'btnTitle':"Update"})


def delete_blog(request, id):
    Post.objects.get(post_id=id).delete()
    return redirect('all-blogs')