import os
from .models import User
from blog.models import *
from django.conf import settings
from django.contrib import messages
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q



def web_login(request):

    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        if not email:
            return render(request, 'accounts/login.html',{"email":email,"password":password})
        if not password:
            return render(request, 'accounts/login.html',{"email":email,"password":password})
        if request.POST.get('remember_me')=='on':    
           request.session.set_expiry(1209600) 
        try:
            user = authenticate(username=email, password=password)
        except Exception as e:
            user = None
        if not user:
            messages.error(request, 'Invalid login details.')

            return render(request, 'accounts/login.html',{"email":email,"password":password})
        
        login(request, user)
        messages.success(request, 'Login in successfully')
        return redirect("accounts:blog_list")

    return render(request, 'accounts/login.html')

@login_required
def log_out_view(request):
    logout(request)
    return redirect('accounts:login')

def web_signup(request):
    if request.method == "POST":


        if User.objects.filter(email = request.POST.get("email")):
            messages.success(request, 'User with this email already exist')
            return render(request, 'accounts/register.html',{"first_name":request.POST.get("first_name") if request.POST.get("first_name") else "",
                                        "last_name":request.POST.get("last_name") if request.POST.get("last_name") else "",
                                        "email":request.POST.get("email") if request.POST.get("email") else ""
                                                            })

        if not request.POST.get("first_name"):
            messages.success(request, 'please enter first name')
            return render(request, 'accounts/register.html',{"first_name":request.POST.get("first_name") if request.POST.get("first_name") else "",
                                        "last_name":request.POST.get("last_name") if request.POST.get("last_name") else "",
                                        "email":request.POST.get("email") if request.POST.get("email") else ""
                                                            })
        if not request.POST.get("last_name"):
            messages.success(request, 'please enter last name')
            return render(request, 'accounts/register.html',{"first_name":request.POST.get("first_name") if request.POST.get("first_name") else "",
                                        "last_name":request.POST.get("last_name") if request.POST.get("last_name") else "",
                                        "email":request.POST.get("email") if request.POST.get("email") else "" })
          
        if not request.POST.get("email"):
            messages.success(request, 'please enter email')
            return render(request, 'accounts/register.html',{"first_name":request.POST.get("first_name") if request.POST.get("first_name") else "",
                                        "last_name":request.POST.get("last_name") if request.POST.get("last_name") else "",
                                        "email":request.POST.get("email") if request.POST.get("email") else ""
                                                            })
        user = User.objects.create(first_name = request.POST.get("first_name"),
                                   last_name = request.POST.get("last_name"),
                                   email = request.POST.get("email"),
                                   password = make_password(request.POST.get("password")))
        
        messages.success(request, 'Registration done successfully')
        return redirect('accounts:web_login')                            
    return render(request, 'accounts/register.html')


def blog_list(request):
    blog_list = Blog.objects.all()
    if request.GET.get("search"):
        blog_list = blog_list.filter(Q(description__icontains = request.GET.get("search"))|Q(title__icontains = request.GET.get("search") ))

    paginator = Paginator(blog_list, 5)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(request , 'blog/blog-list.html',{"blog_list":page_obj,"search":"search",
                                                   "search_value":request.GET.get("search") if request.GET.get("search") else "" })
