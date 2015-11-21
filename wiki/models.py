# -*- coding: utf-8 -*-

from django.db import models
from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import redirect, render
from django.http import HttpResponseRedirect

class Article(models.Model):
    class Meta:
        verbose_name = u'wiki'
        ordering = ['title']

    title = models.CharField(verbose_name=u'title', max_length=256)
    subtitle = models.CharField(verbose_name=u'subtitle', max_length=256, default='')
    content = models.TextField(u'content', blank=True, default='')
    created = models.DateTimeField(auto_now_add=True, verbose_name=u'date')
    last_modified = models.DateTimeField(auto_now_add=True, null=True, verbose_name=u'modified')

    def __unicode__(self):
        return self.title

def search(request):
    req_title = request.POST['title']
    try:
        Article.objects.get(title=req_title)
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('wikiarticle', kwargs={'pk': req_title}))
    else:
        return HttpResponseRedirect(reverse('wikiarticle', kwargs={'pk': req_title}))