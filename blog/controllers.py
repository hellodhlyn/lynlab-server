# -*- coding: utf-8 -*-

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.admin.views.decorators import staff_member_required
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from django_ajax.decorators import ajax

from .models import Post, Category, PostType, PostTypeRelation


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
