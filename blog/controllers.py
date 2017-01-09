# -*- coding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_ajax.decorators import ajax

from .models import *


def get_client_ip(request):
    """
    Get IP address of client user.
    """
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def is_recent_visitor(timestamp):
    """
    Check if the visitor visited in recent 7 days.
    """
    now = datetime.datetime.utcnow().replace(tzinfo=utc)
    timediff = now - timestamp
    if timediff.total_seconds() < (60 * 60 * 24) * 7:
        return True
    else:
        return False


@csrf_exempt
def load_posts(request):
    page = int(request.POST.get('page'))
    filters = request.POST.get('filters').split(',')[:-1]

    key = request.POST.get('key')
    value = request.POST.get('value')

    try:
        if key and value and len(key) > 0 and len(value) > 0:
            key = key.lower()
            value = value.lower()

            if key == 'tag':
                posts = sorted(map(lambda x: x.post, PostTagRelation.objects.filter(tag=Tag.objects.get(url=value))),
                               key=lambda y: y.id, reverse=True)
            elif key == 'category':
                posts = Post.objects.filter(category=Category.objects.get(url=value)).order_by('-created')
            else:
                raise Exception()
        else:
            raise Exception()
    except ObjectDoesNotExist:
        posts = []
    except:
        posts = Post.objects.filter(public_post=True).order_by('-created')

    start = (page - 1) * 10
    end = min(page * 10, len(posts))

    response_posts = posts[start:end]
    # -------------- TEMPORARILY DISABLED --------------
    #
    # for p in posts[start:end]:
    #     filter_num = 0
    #     for f in filters:
    #         filter_num += PostTypeRelation.objects.filter(type_id=f, post_id=p.id).count()
    #     if filter_num == 0:
    #         response_posts.append(p)
    #
    # --------------------------------------------------

    context = {
        'posts': response_posts,
    }

    return render(request, 'blog/posts.html', context)


@ajax
def like_post(request, id):
    post = Post.objects.get(id=int(id))
    address = get_client_ip(request)

    likes = sorted(PostLikeAddress.objects.filter(post=post, address=address), key=lambda like: like.timestamp,
                   reverse=True)
    if len(likes) > 0 and not is_recent_visitor(likes[0].timestamp):
        return post.like_count

    like_instance = PostLikeAddress(post=post, address=address)
    like_instance.save()

    post.like_count += 1
    post.save()

    return post.like_count


@ajax
def unlike_post(request, id):
    post = Post.objects.get(id=int(id))
    address = get_client_ip(request)

    if len(PostLikeAddress.objects.filter(post=post, address=address)) == 0:
        return post.like_count

    PostLikeAddress.objects.filter(post=post, address=address).delete()

    post.like_count -= 1
    post.save()

    return post.like_count
