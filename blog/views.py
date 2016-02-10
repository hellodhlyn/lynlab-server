# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from .models import Post, PostType, Category

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

def main(request):
    template_name = 'blog/home.html'

    context = {
        'types': PostType.objects.all(),
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))