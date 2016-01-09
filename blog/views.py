# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from blog.models import Post, Category

def handler404(request):
    response = render_to_response('404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response

class PostDetail(DetailView):
    model = Post
    template_name = 'blog/detail.html'

class PostCreate(CreateView):
    model = Post
    template_name = 'create.html'

def show_posts(request):
    template_name = 'blog/home.html'
    paged_template_name = 'blog/home_with_paged.html'

    context = {
        'posts': Post.objects.all().order_by('-created'),
        'page_template': paged_template_name
    }

    if request.is_ajax():
        template_name = paged_template_name

    return render_to_response(template_name, context, context_instance=RequestContext(request))