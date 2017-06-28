import twitter
from dateutil import parser
from django.conf import settings
from django.contrib import admin as djangoadmin
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render

from .models import *


@staff_member_required
def admin(request):
    template_name = 'blog/admin/admin.html'
    context = {
        'posts': Post.objects.all().order_by('-created'),
        'series_list': Series.objects.all(),
    }

    return render(request, template_name, context)


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

        return render(request, template_name, context)

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

        return render(request, template_name, context)

    elif request.method == 'POST':
        return __modify_post(request)


@staff_member_required
def __modify_post(request):
    def __modify_tags(post, tags):
        if tags is None or len(tags) is 0:
            return

        for url in tags.split(','):
            try:
                tag = Tag.objects.get(url=url)
            except ObjectDoesNotExist:
                tag = Tag(url=url)
                tag.save()

            try:
                PostTagRelation.objects.get(post=post, tag=tag)
            except ObjectDoesNotExist:
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

    # ID에 해당하는 포스트를 가져온다. ID가 없을 경우 (i.e. 신규일 경우) 에는 새로운 인스턴스를 만든다.
    try:
        post = Post.objects.get(id=req_id)
    except ValueError:
        post = Post()
    except ObjectDoesNotExist:
        post = Post()

    post.title = req_title or '제목이 없습니다'
    post.content = req_content or ''
    post.description = req_description or '설명이 없습니다'
    post.category = Category.objects.get(url=req_category)
    post.tags = req_old_tags or ''
    post.series_id = None if int(req_series_id) == -1 else int(req_series_id)
    post.posttype = req_posttype or '0'
    post.preview = req_preview or ''
    post.public_post = (req_public_post == 'on')
    post.save()

    # 태그를 설정한다.
    __modify_tags(post, req_tags)

    for t in PostType.objects.all():
        req_type = request.POST.get('type' + str(t.id))
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

    template_name = 'blog/admin/create_tweet.html'
    context = {
        'post': post,
    }

    return render(request, template_name, context)


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
    list_display_links = None
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
