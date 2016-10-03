# -*- coding: utf-8 -*-

from django.contrib import admin as djangoadmin
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.conf import settings
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext

from dateutil import parser

from .models import *

import twitter

@staff_member_required
def admin(request):
    template_name = 'blog/admin/admin.html'

    context = {
        'posts': Post.objects.all().order_by('-created'),
        'series_list': Series.objects.all(),
    }

    return render_to_response(template_name, context, context_instance=RequestContext(request))

@staff_member_required
def create_post(request):
    if request.method == 'GET':
        template_name = 'blog/admin/modify.html'

        all_types = PostType.objects.all()
        post_types = [False] * len(all_types)

        context = {
            'types': zip(all_types, post_types),
            'categories': Category.objects.all(),
            'tags': Tag.objects.all(),
            'series_list': Series.objects.all(),
        }

        return render_to_response(template_name, context, context_instance=RequestContext(request))

    elif request.method == 'POST':
        return __modify_post(request)

@staff_member_required
def modify_post(request, pk):
    if request.method == 'GET':
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
            'categories': Category.objects.all(),
            'tags': Tag.objects.all(),
            'series_list': Series.objects.all(),
        }

        return render_to_response(template_name, context, context_instance=RequestContext(request))

    elif request.method == 'POST':
        return __modify_post(request)

@staff_member_required
def __modify_post(request):
    def __migrate_tags(post, old_tags):
        for tag_name in old_tags.split(','):
            tag_name = tag_name.lower()
            try:
                tag = Tag.objects.get(url=tag_name)
            except:
                tag = Tag(url=tag_name)
                tag.save()

            PostTagRelation(post=post, tag=tag).save()

    def __modify_tags(post, tags):
        current_tags = PostTagRelation.objects.filter(post=post)

        for url in tags.split(','):
            tag = None
            try:
                tag = Tag.objects.get(url=url)
            except:
                tag = Tag(url=url)
                tag.save()

            try: 
                PostTagRelation.object.get(post=post, tag=tag)
            except:
                PostTagRelation(post=post, tag=tag).save()


    req_id = request.POST.get('id')
    req_title = request.POST.get('title')
    req_content = request.POST.get('content')
    req_description = request.POST.get('description')
    req_category = request.POST.get('category')
    req_old_tags = request.POST.get('tags')
    req_tags = request.POST.get('new_tags')
    req_series_id = request.POST.get('series')
    req_posttype = request.POST.get('posttype')
    req_preview = request.POST.get('preview')
    req_public_post = request.POST.get('public_post', False)

    try:
        post = Post.objects.get(id=req_id)

        if PostTagRelation.objects.filter(post=post).count() == 0:
            __migrate_tags(post, req_old_tags)
            req_old_tags = ''
    except ValueError:
        post = Post()
    except ObjectDoesNotExist:
        post = Post()

    __modify_tags(post, req_tags)
    post.title = req_title or '제목이 없습니다'
    post.content = req_content or ''
    post.description = req_description or '설명이 없습니다'
    post.category = Category.objects.get(url=req_category)
    post.tags = req_old_tags or ''
    post.series_id = None if int(req_series_id) == -1 else int(req_series_id)
    post.posttype = req_posttype or '0'
    post.preview = req_preview or ''
    post.public_post = req_public_post
    post.save()

    for t in PostType.objects.all():
        req_type = request.POST.get('type'+str(t.id))
        if req_type:
            related = PostTypeRelation.objects.filter(post_id=post.id, type_id=t.id)
            if len(related) == 0:
                PostTypeRelation(post_id=post.id, type_id=t.id).save()
        else:
            related = PostTypeRelation.objects.filter(post_id=post.id, type_id=t.id)
            if len(related) != 0:
                related[0].delete()

    messages.add_message(request, messages.SUCCESS, u'포스트가 성공적으로 추가/수정되었습니다.')

    if 'submit_save' in request.POST:
        return redirect(reverse('blog-admin-modify-post', kwargs={'pk': post.id}))
    elif 'submit_complete' in request.POST:
        return redirect(reverse('blogadmin'))

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
def series(request):
    # 시리즈를 생성한다
    if request.method == 'POST':
        name = request.POST.get('name')

        series = Series(name=name)
        series.save()

        message_body = u'시리즈 \' ' + name + u'\'이(가) 성공적으로 생성되었습니다.'
        messages.add_message(request, messages.SUCCESS, message_body)

    return redirect(reverse('blogadmin'))

@staff_member_required
def modify_series(request, id):
    return None


class PostTypeAdmin(djangoadmin.ModelAdmin):
    list_display = ['id', 'name', 'icon', 'default']
    list_editable = ['name', 'default']
    search_fields = ['name']
    ordering = ['name']

class CategoryAdmin(djangoadmin.ModelAdmin):
    list_display = ['name']
    list_editable = ['name']
    search_fields = ['name']
    ordering = ['name']

class TagAdmin(djangoadmin.ModelAdmin):
    list_display = ['id', 'url']
    list_editable = ['url']
    ordering = ['id']

class TagTranslationsAdmin(djangoadmin.ModelAdmin):
    list_display = ['id', 'tag', 'name', 'language']
    list_editable = ['name']
    ordering = ['tag']

class PostTagRelationAdmin(djangoadmin.ModelAdmin):
    list_display = ['tag', 'post']
    ordering = ['post']

djangoadmin.site.register(PostType, PostTypeAdmin)
djangoadmin.site.register(Category, CategoryAdmin)
djangoadmin.site.register(Tag, TagAdmin)
djangoadmin.site.register(TagTranslations, TagTranslationsAdmin)
djangoadmin.site.register(PostTagRelation, PostTagRelationAdmin)
