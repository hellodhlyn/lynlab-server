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
        post_item = Post.objects.get(id=pk)
    except ObjectDoesNotExist:
        raise Http404()

    if not post_item.public_post:
        raise Http404()

    # Increment hit count for first visit (by s ession)
    hit_key = f"hit-post-{post_item.id}"
    if hit_key not in request.session:
        post_item.hitcount += 1
        post_item.save()

        request.session[hit_key] = 1

    context = {
        'post': post_item
    }

    return render(request, 'blog/post.html', context)
