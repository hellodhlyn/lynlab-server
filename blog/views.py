from django.core.exceptions import ObjectDoesNotExist
from django.core.paginator import Paginator
from django.http import Http404
from django.shortcuts import render

from .models import *


def index(request):
    """
    List all posts.

    Query param =>
      category: (int) ID of category.
    """
    post_filters = {'public_post': True}
    if request.GET.get('category'):
        post_filters['category'] = request.GET['category']
    post_list = Post.objects.filter(**post_filters).order_by('-created')

    page = request.GET.get('page', 1)
    context = {
        'post_filters': post_filters,
        'posts': Paginator(post_list, 20).get_page(page),
    }

    return render(request, 'blog/index.html', context)


def post(request, pk):
    """
    Get a post.
    """
    try:
        post = Post.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404()

    if not post.public_post:
        raise Http404()

    context = {
        'post': post
    }

    return render(request, 'blog/post.html', context)
