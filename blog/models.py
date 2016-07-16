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

# 포스트 카테고리.
class Category(models.Model):
    class Meta:
        verbose_name = u'category'
        ordering = ['name']

    name = models.CharField(verbose_name=u'name', max_length=50)
    url = models.CharField(max_length=32, default='')

    def __unicode__(self):
        return self.name

# 포스트의 유형. 필터링을 위해 사용된다.
class PostType(models.Model):
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    default = models.BooleanField(default=True)

# 포스트의 시리즈.
class Series(models.Model):
    name = models.CharField(max_length=30, default='')

    def post_num(self):
        return Post.objects.filter(series=self).count()

# 포스트.
class Post(models.Model):
    class Meta:
        verbose_name = u'post'
        ordering = ['created']

    # Meta infos
    category = models.ForeignKey(Category, verbose_name=u'category', null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'date')
    preview = models.CharField(verbose_name=u'preview', null=True, blank=True, max_length=256)
    tags = models.TextField(max_length=256, default='')
    hitcount = models.IntegerField(default=0)
    series = models.ForeignKey(Series, related_name='posts', null=True)

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

# 포스트의 종류의 다대다 관계 테이블.
class PostTypeRelation(models.Model):
    post_id = models.IntegerField()
    type_id = models.IntegerField()

# 포스트 조회수.
class PostHitAddress(models.Model):
    post = models.ForeignKey(Post)
    address = models.TextField(max_length=16, default='')
    timestamp = models.DateTimeField(auto_now_add=True)
