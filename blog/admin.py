# -*- coding: utf-8 -*-

from django.contrib import admin as djangoadmin
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext

from dateutil import parser

from .models import Post, Category, PostType, PostTypeRelation

import twitter

@staff_member_required
def admin(request):
    template_name = 'blog/admin/admin.html'

    context = { 
        'posts': Post.objects.all().order_by('-created'),
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))

@staff_member_required
def create_tweet(request):
    api = twitter.Api(consumer_key=settings.TWITTER_KEY,
                      consumer_secret=settings.TWITTER_SECRET,
                      access_token_key=settings.TWITTER_ACCESS_KEY,
                      access_token_secret=settings.TWITTER_ACCESS_SECRET)

    tweet_id = request.POST.get('tweet_id')
    tweet = api.GetStatus(tweet_id)
    tweet_time = parser.parse(tweet.created_at).strftime('%Y년 %m월 %d일 %I:%M %p')

    post = {
        'posttype': 'tweet',
        'created': tweet_time,
        'content': tweet.text,
        'tags': tweet.id,
    }

    print tweet

    template_name = 'blog/admin/create_tweet.html'
    context = {
        'post': post,
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))

@staff_member_required
def create_post(request):
    template_name = 'blog/admin/modify.html'

    context = {
        'types': PostType.objects.all(),
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))

@staff_member_required
def modify_post(request, pk):
    template_name = 'blog/admin/modify.html'
    post = Post.objects.filter(id=pk)

    all_types = PostType.objects.all()
    post_types = []
    for t in all_types:
        if PostTypeRelation.objects.filter(post_id=pk, type_id=t.id).count() == 0:
            post_types.append(False)
        else:
            post_types.append(True)

    context = {
        'post': post[0],
        'types': zip(all_types, post_types),
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))

class PostTypeAdmin(djangoadmin.ModelAdmin):
    list_display = ['id', 'name', 'icon', 'default']
    list_editable = ['name', 'default']
    search_fields = ['name']
    ordering = ['name']

djangoadmin.site.register(PostType, PostTypeAdmin)