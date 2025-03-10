from django.shortcuts import get_object_or_404, redirect, render
from .models import*
from django.db.models import Count
from django.core.paginator import Paginator

def index(request):
    userid =request.session.get('userid')
    post = blog.objects.order_by('-id')
    mainpost = blog.objects.filter(status='1').annotate(comment_count=Count('comments')).order_by('-comment_count', '-id')[:1]
    for i in mainpost:
        mainpostSlug = i.blog_slug
    try:    
        mpobj = get_object_or_404(blog, blog_slug = mainpostSlug)
        mpCommentCount = comments.objects.filter(post = mpobj).count()
    except:
        return render(request,'index.html')
    # print(mpCommentCount)
    otherpost = blog.objects.filter(status = '1').exclude(blog_slug = mainpostSlug).annotate(comment_count=Count('comments')).order_by('-id')   
    paginator = Paginator(otherpost, 6)
    page_number = request.GET.get('page')
    pageObj = paginator.get_page(page_number)
    cat = category.objects.all()
    print(pageObj)
    context = {
        'post':post,
        'main_post':mainpost,
        'category':cat,
        'otherposts':pageObj,
        "mainCommentCount":mpCommentCount,
        "userid":userid,
        'pageobj':pageObj
    }
    return render(request,'index.html',context)

def blog_details(request,slug):
    userid =request.session.get('userid')
    post = get_object_or_404(blog,blog_slug = slug)
    cat = category.objects.all()
    related_post = blog.objects.filter(category = post.category).exclude(blog_slug = slug).order_by('-id')
    commnt = comments.objects.filter(post=post).order_by("-date_time")
    context = {
        'post':post,
        'category':cat,
        'relatedPost':related_post,
        "comments":commnt,
        "userid":userid
    }
    return render(request,'blog_details.html',context)

def cat(request,slug):
    userid =request.session.get('userid')
    cats = category.objects.all()
    # post_category = get_object_or_404(category,slug = slug)
    post_category = category.objects.get(slug = slug)
    catname = post_category.name
    cposts = blog.objects.filter(category = post_category, status = '1').annotate(comment_counts = Count('comments')).order_by("-id")
    paginator = Paginator(cposts,10)
    page_number = request.GET.get('page')
    pageobj = paginator.get_page(page_number)
    context = {
        'category':cats,
        "catName":catname,
        "categoryPost":pageobj,
        "userid":userid,
        'pageobj':pageobj
    }
    return render(request,"category.html",context)

def addcomment(request,slug):
    userid = request.session.get('userid')
    if request.method == "POST":
        post = get_object_or_404(blog,blog_slug=slug)
        comment = request.POST.get("comment")
        name = request.POST.get("name")
        email = request.POST.get("email")
        website = request.POST.get("website")
        userobj = get_object_or_404(user,id=userid)

        comments.objects.create(
            post = post,
            comment = comment,
            name = name,
            email = email,
            website = website,
            user = userobj
        )

        return redirect('blogdetails', slug = post.blog_slug)
    return redirect('blogdetails')

def userRegister(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        if user.objects.filter(username=username).exists():
            return render(request,"signup.html",{'error':'username already exists'})
        
        user.objects.create(
            name = name,
            username = username,
            password = password,
            email = email
        )
        return redirect('login')     
    return render(request,"signup.html")

def login(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            userobj = user.objects.get(username=username,password=password)
            request.session['userid'] = userobj.id
            return redirect('index')
        except user.DoesNotExist:
            return render(request,"login.html",{'error':'Invalid Username/Password'})
    return render(request,'login.html')

def addBlog(request):
    authorid = request.session.get('userid')
    if request.method == 'POST':
        author = get_object_or_404(user,id = authorid )
        title = request.POST.get('title')
        image = request.FILES.get('image')
        cats = request.POST.get('category')
        content = request.POST.get('content')
        status = request.POST.get('status')
        catobj = get_object_or_404(category,slug=cats)
        print(image,title,cats,content,status,author,catobj)
        blog.objects.create(
            author = author,
            title = title,
            content = content,
            image = image,
            category = catobj,
            status = status,
        )
        return redirect('userpost')
    cat = category.objects.all()
    return render(request,'postblog.html',{'category':cat,"userid":authorid})

def userpost(request):
    print('userpost')
    userid = request.session.get('userid')
    userobj = get_object_or_404(user,id=userid)
    posts = blog.objects.filter(author = userobj).annotate(comment_counts = Count('comments')).order_by('-updated_at')
    cat = category.objects.all()
    context = {
        'posts':posts,
        'category':cat
    }
    return render(request,'userpost.html',context)

def userManagePost(request,slug):
    print('userManagePost')
    userid =request.session.get('userid')
    post = get_object_or_404(blog,blog_slug = slug)
    cat = category.objects.all()
    commnt = comments.objects.filter(post=post).order_by("-date_time")
    context = {
        'post':post,
        'category':cat,
        "comments":commnt,
        "userid":userid
    }
    return render(request,"userManagePost.html",context)

def deleteComment(request,cid):
    comment = get_object_or_404(comments,id = cid)
    comment.delete()
    return redirect('umanagepost',slug = comment.post.blog_slug)

def deletePost(request,pid):
    post = get_object_or_404(blog,id = pid)
    post.delete()
    return redirect('userpost')

def editPost(request,slug):
    post = get_object_or_404(blog,blog_slug = slug)
    cat = category.objects.all()
    if request.method == "POST":
        post.title = request.POST.get('title')
        if request.FILES.get('image'):
            post.image = request.FILES.get('image')
        post.content = request.POST.get('content')
        post.status = request.POST.get('status')
        post.save()
        return redirect('umanagepost',slug=slug)
    context = {
        'post':post,
        'category':cat
    }
    return render(request,'editPost.html',context)

def logout(request):
    del request.session['userid']
    return redirect('index')