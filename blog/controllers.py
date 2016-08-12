# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django_ajax.decorators import ajax

from .models import *


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

@csrf_exempt
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

@ajax
def like_post(request, id):
    post = Post.objects.get(id=int(id))
    address = get_client_ip(request)

    if len(PostLikeAddress.objects.filter(post=post, address=address)) > 0:
      return post.like_count

    like_instance = PostLikeAddress(post=post, address=address)
    like_instance.save()

    post.like_count = post.like_count + 1
    post.save()

    return post.like_count

@ajax
def unlike_post(request, id):
    post = Post.objects.get(id=int(id))
    address = get_client_ip(request)

    if len(PostLikeAddress.objects.filter(post=post, address=address)) == 0:
      return post.like_count

    like_instance = PostLikeAddress.objects.filter(post=post, address=address).delete()

    post.like_count = post.like_count - 1
    post.save()

    return post.like_count