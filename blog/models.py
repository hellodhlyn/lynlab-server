# -*- coding: utf-8 -*-

import datetime

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import admin
from django.contrib.admin.views.decorators import staff_member_required
from django.db import models
from django.utils.timezone import utc
from django.http import HttpResponseRedirect

from django_markup.filter import MarkupFilter

class Category(models.Model):
    class Meta:
        verbose_name = u'category'
        ordering = ['name']
    
    name = models.CharField(verbose_name=u'name', max_length=50)
    
    def __unicode__(self):
        return self.name


class Post(models.Model):
    class Meta:
        verbose_name = u'post'
        ordering = ['created']
    
    # Meta infos
    category = models.ForeignKey(Category, verbose_name=u'category', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'date')
    preview = models.CharField(verbose_name=u'preview', null=True, blank=True, max_length=256)
    tags = models.TextField(max_length=256, default='')
    
    # Detail infos
    title = models.CharField(u'title', max_length=256)
    description = models.TextField(u'description', blank=True, default='')
    content = models.TextField(u'content', blank=True, default='')

    # Options
    public_post = models.BooleanField(default=False)

    # Types (0: general post / 1: notify post)
    posttype = models.CharField(u'posttype', null=False, max_length=20)
    
    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('detail', kwargs={'pk': self.id})

    def is_recent_post(self):
        if self.created:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - self.created
            if timediff.total_seconds() < 86400:
                return True
            else:
                return False

    def split_tags(self):
        if self.tags == '':
            return [u'태그 없음']
        else:
            return self.tags.split(',')

@staff_member_required
def create(request):
    req_posttype = request.POST.get('posttype')
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

    
    post.posttype = req_posttype
    post.title = req_title or '제목이 없습니다'
    post.content = req_content or None
    post.description = req_description or '설명이 없습니다'
    post.tags = req_tags or None
    post.preview = req_preview or None
    post.public_post = req_public_post
    post.save()

    return HttpResponseRedirect(reverse('blogadmin'))
