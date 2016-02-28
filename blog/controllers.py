# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render

from django_ajax.decorators import ajax

from .models import Post, PostType, PostTypeRelation

@staff_member_required
def create(request):
    req_id = request.POST.get('id')
    req_title = request.POST.get('title')
    req_content = request.POST.get('content')
    req_description = request.POST.get('description')
    req_tags = request.POST.get('tags')
    req_preview = request.POST.get('preview')
    req_public_post = request.POST.get('public_post', False)

    try:
        post = Post.objects.get(id=req_id)
    except ValueError:
        post = Post()
    except ObjectDoesNotExist:
        post = Post()

    post.title = req_title or '제목이 없습니다'
    post.content = req_content or None
    post.description = req_description or '설명이 없습니다'
    post.tags = req_tags or None
    post.preview = req_preview or None
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

    return HttpResponseRedirect(reverse('blogadmin'))

def load_posts(request):
    page = int(request.POST.get('page'))
    filters = request.POST.get('filters').split(',')[:-1]

    posts = Post.objects.order_by('-created')

    start = (page-1)*10
    end = min(page*10, len(posts))

    response_posts = []
    for p in posts[start:end]:
        filter_num = 0
        for f in filters:
            filter_num += PostTypeRelation.objects.filter(type_id=f, post_id=p.id).count()
        if filter_num == 0:
            response_posts.append(p)

    context = {
        'posts': response_posts,
    }

    return render(request, 'blog/posts.html', context)