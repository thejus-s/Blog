from django.shortcuts import get_object_or_404, render
from .models import*
def index(request):
    post = blog.objects.order_by('-id')
    mainpost = blog.objects.order_by('-id').filter(main_post = True)[0:1]
    cat = category.objects.all()
    
    context = {
        'post':post,
        'main_post':mainpost,
        'category':cat
    }
    return render(request,'index.html',context)

def blog_details(request,slug):
    post = get_object_or_404(blog,blog_slug = slug)
    cat = category.objects.all()
    context = {
        'post':post,
        'category':cat
    }

    return render(request,'blog_details.html',context)