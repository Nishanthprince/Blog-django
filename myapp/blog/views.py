from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
import logging
from .models import Post,AboutUs
from django.http import Http404
from django.core.paginator import Paginator
from .forms import ContactForm

#create your views here
# static demo data
#posts=[
#      {'id':1,'title':'post of 1', 'content':'content of post 1'},
#      {'id':2,'title':'post of 2', 'content':'content of post 2'},
#      {'id':3,'title':'post of 3', 'content':'content of post 3'},
#      {'id':4,'title':'post of 4', 'content':'content of post 4'},
#      {'id':5,'title':'post of 5', 'content':'content of post 5'},
#      {'id':6,'title':'post of 6', 'content':'content of post 6'},
#   ]


# Create your views here.
def index(request):
    blog_title="Latest post"
    #getting data from post model
    all_posts = Post.objects.all()

    paginator = Paginator(all_posts,5)
    page = request.GET.get('page')
    page_obj = paginator.get_page(page)

    return render(request,'blog/index.html',{'blog_title':blog_title , 'page_obj':page_obj})

def detail(request,slug):
    #static data
    #post= next((item for item in posts if item['id']== int(post_id)),None)
    try:
    #getting data from model by post_id 
        post=Post.objects.get(slug=slug)
        related_posts = Post.objects.filter(category = post.category).exclude(pk=post.id)

    except Post.DoesNotExist:
        raise Http404("Post Does Not Exist")


    return render(request,'blog/detail.html',{'post':post, 'related_posts':related_posts})

def old_url_redirect(request):
    return redirect(reverse('blog:new_page_url'))

def new_url_view(request):
    return HttpResponse("this is the new url")

def contact_view(request):
    if request.method =='POST':
        form = ContactForm(request.POST)
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        logger = logging.getLogger("TESTING")
        if form.is_valid():
            logger.debug(f'post data is {form.cleaned_data['name']} {form.cleaned_data['email']} {form.cleaned_data['message']}')
            success_message = 'YOUR EMAIL HAS BEEN SEND...!'
            # SEND EMAIL OR SAVE IN DATABASE
            return render(request,'blog/contact.html',{'form':form,'success_message':success_message})
        else:
            logger.debug('FORM validation failure..!')
        return render(request,'blog/contact.html',{'form':form,'name':name,'email':email,'message':message})
    return render(request,'blog/contact.html')

def about_view(request):
    about_content =AboutUs.objects.first().content
    return render(request,'blog/about.html',{'about_content':about_content})



