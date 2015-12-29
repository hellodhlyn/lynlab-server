# -*- coding: utf-8 -*-

import os
import binascii

from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect

from difflib import Differ

class Article(models.Model):
    class Meta:
        verbose_name = u'wiki'
        ordering = ['title']

    title = models.CharField(verbose_name=u'title', max_length=256)
    subtitle = models.CharField(verbose_name=u'subtitle', max_length=256, blank=True, default='')
    content = models.TextField(u'content', blank=True, default='')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'date')
    last_modified = models.DateTimeField(auto_now_add=True, null=True, verbose_name=u'modified')

    # state code 200: normal, 303: see other
    code = models.IntegerField(u'code', default=200)

    def __unicode__(self):
        return self.title

class ModifyHistory(models.Model):
    class Meta:
        verbose_name = u'wiki_history'
        ordering = ['timestamp']

    # state code 0: modify, 1: created, 9: deleted
    state = models.IntegerField(u'state', default=0, null=False)
    code = models.CharField(u'code', max_length=64, default='')
    title = models.CharField(verbose_name=u'title', max_length=256)
    timestamp = models.DateTimeField(verbose_name=u'timestamp', auto_now_add=True)
    editor = models.CharField(verbose_name=u'editor', max_length=256)
    diff = models.TextField(u'diff', blank=True, default='')

def search(request):
    req_title = request.POST['title']
    try:
        Article.objects.get(title=req_title)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('wikiarticle', kwargs={'pk': req_title}))
    else:
        return HttpResponseRedirect(reverse('wikiarticle', kwargs={'pk': req_title}))

@login_required(login_url='/accounts/login/')
def modify(request):
    if request.user.is_authenticated():
        username = request.user.username
    else:
        return HttpResponse(status=201)

    req_title = request.POST.get('title', False)
    req_content = request.POST.get('content', False)

    res_code = 200
    if request.POST.get('redirect', False):
        res_code = 303

    try:
        article = Article.objects.get(title=req_title)
    except ObjectDoesNotExist:
        new_article = Article(title=req_title, content=req_content, code=res_code)
        new_article.save()
        diff = req_content
    else:
        d = Differ()
        diff_list = list(d.compare(article.content.splitlines(1), req_content.splitlines(1)))
        diff = '\n'.join(diff_list)

        article.content = req_content
        article.code = res_code
        article.save()

    new_history = ModifyHistory(title=req_title, editor=username, diff=diff, code=gen_code())
    new_history.save()

    return HttpResponseRedirect(reverse('wikiarticle', kwargs={'pk': req_title}))

def gen_code():
    return binascii.hexlify(os.urandom(16))