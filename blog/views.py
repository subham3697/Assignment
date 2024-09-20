from django.shortcuts import render , redirect
from .models import *
from django.urls import reverse
from django.core.mail import send_mail
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.http import JsonResponse
from django.contrib import messages


def blog_detail(request,id):
    blog_details = Blog.objects.get(id = id)
    blog_comments = BlogComment.objects.filter(blog = blog_details)
    return render(request, "blog/blog-details.html",{"blog_details":blog_details,
                                                     "blog_comments":blog_comments})


def add_comment(request,id):
    blog_details = Blog.objects.get(id = id)
    blog_comments = BlogComment.objects.filter(blog = blog_details)

    comment = BlogComment.objects.create(
        comment = request.POST.get("comment"),
        blog = blog_details,
        created_by = request.user
    )
    url = reverse('blog:blog_detail', kwargs={'id': id})
    return redirect(url)



def like_blog(request):
    if request.method == "POST":
        blog_id = request.POST.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id)
        
        if request.user in blog.likes.all():
            blog.likes.remove(request.user)
            liked = False
        else:
            blog.likes.add(request.user)
            liked = True
        
        return JsonResponse({
            'liked': liked,
            'total_likes': blog.likes.count()
        })




def share_blog(request):
    if request.method == 'POST':
        blog_id = request.POST.get('blog_id')
        blog = get_object_or_404(Blog, id=blog_id)
        
        subject = f"Check out this blog: {blog.title}"
        message = f"Hi there,\n\nI thought you might like this blog: {blog.title}.\nYou can read it here: {request.build_absolute_uri(blog.get_absolute_url())}\n\nEnjoy!"
        from_email = settings.DEFAULT_FROM_EMAIL
        recipient_list = [request.user.email]  
        print(recipient_list)
     
        send_mail(subject, message, from_email, recipient_list)
        messages.error(request, 'Email send successfully')
    return redirect('accounts:blog_list')

