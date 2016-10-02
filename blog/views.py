# -*- coding: utf-8 -*-

from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.utils import translation

from .models import *
from .controllers import get_client_ip, is_recent_visitor


class PostCreate(CreateView):
	model = Post
	template_name = 'create.html'

def main(request):
	template_name = 'blog/home.html'

	context = {
		'types': PostType.objects.all(),
	}

	return render_to_response(template_name, context, context_instance=RequestContext(request))

def by_tag(request, tag):
	template_name = 'blog/home.html'

	context = {
		'search_tag': tag,
		'types': PostType.objects.all(),
	}

	return render_to_response(template_name, context, context_instance=RequestContext(request))

def post_detail(request, pk):
	post = None 
	try:
		post = Post.objects.get(id=pk)
		if post.public_post is False:
			raise Http404
	except ObjectDoesNotExist:
		raise Http404

	address = get_client_ip(request)

	# Increase the hit count
	hits = sorted(PostHitAddress.objects.filter(post=post, address=address), key=lambda hit: hit.timestamp, reverse=True)
	if len(hits) == 0 or not is_recent_visitor(hits[0].timestamp):
		post.hitcount = post.hitcount + 1
		post.save()

		hit_instance = PostHitAddress(post=post, address=address)
		hit_instance.save()

	# Get liked info
	likes = sorted(PostLikeAddress.objects.filter(post=post, address=address), key=lambda like: like.timestamp, reverse=True)
	liked = len(likes) > 0 and is_recent_visitor(likes[0].timestamp)

	# Get the content and make context
	context = {
		'post': post,
		'liked': liked,
	}

	return render(request, 'blog/detail.html', context, context_instance=RequestContext(request))