# -*- coding: utf-8 -*-

from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, render_to_response
from django.template import RequestContext

from .models import *
from .controllers import get_client_ip


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
	post = Post.objects.get(id=pk)
	ip = get_client_ip(request)

	# Increase the hit count
	if len(PostHitAddress.objects.filter(post=post, address=ip)) == 0:
		post.hitcount = post.hitcount + 1
		post.save()

		hit_instance = PostHitAddress(post=post, address=ip)
		hit_instance.save()

	liked = len(PostLikeAddress.objects.filter(post=post, address=ip)) > 0

	# Get the content and make context
	context = {
		'post': post,
		'liked': liked,
	}

	return render(request, 'blog/detail.html', context, context_instance=RequestContext(request))