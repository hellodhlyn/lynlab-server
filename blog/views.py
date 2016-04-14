# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from .models import *


class PostCreate(CreateView):
	model = Post
	template_name = 'create.html'

def main(request):
	template_name = 'blog/home.html'

	context = {
		'types': PostType.objects.all(),
	}

	return render_to_response(template_name, context, context_instance=RequestContext(request))

def post_detail(request, pk):
	context = {
		'post': Post.objects.get(id=pk)
	}

	return render(request, 'blog/detail.html', context, context_instance=RequestContext(request))