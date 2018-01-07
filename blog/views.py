from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404
from django.shortcuts import render

from .controllers import get_client_ip, is_recent_visitor
from .models import *


def main(request):
    """
    List of all posts. (/)
    """
    template_name = 'blog/home.html'
    context = {'types': PostType.objects.all()}

    return render(request, template_name, context)


def by_tag(request, tag):
    """
    Get list of posts filtered by a tag. (/tag/{tag})
    :param request:
    :param tag: URL query {tag}
    """
    template_name = 'blog/home.html'
    context = {
        'search_tag': tag,
        'types': PostType.objects.all(),
    }

    return render(request, template_name, context)


def by_category(request, category):
    """
    Get list of posts filtered by a category. (/category/{category})
    :param request:
    :param category: URL query {category}
    """
    template_name = 'blog/home.html'
    context = {
        'search_category': category,
        'types': PostType.objects.all(),
    }

    return render(request, template_name, context)


def post_detail(request, pk):
    """
    Get detail of the post. (/{pk})
    :param request:
    :param pk: ID of the post, URL query {pk}
    """
    try:
        post = Post.objects.get(id=pk)
        if post.public_post is False:
            raise Http404
    except ObjectDoesNotExist:
        raise Http404

    address = get_client_ip(request)

    # Increase the hit count
    hits = sorted(PostHitAddress.objects.filter(post=post, address=address), key=lambda hit: hit.timestamp,
                  reverse=True)
    if len(hits) == 0 or not is_recent_visitor(hits[0].timestamp):
        post.hitcount += 1
        post.save()

        hit_instance = PostHitAddress(post=post, address=address)
        hit_instance.save()

    # Get liked info
    likes = sorted(PostLikeAddress.objects.filter(post=post, address=address), key=lambda like: like.timestamp,
                   reverse=True)
    liked = len(likes) > 0 and is_recent_visitor(likes[0].timestamp)

    # Get the content and make context
    context = {
        'post': post,
        'liked': liked,
    }

    return render(request, 'blog/detail.html', context)
