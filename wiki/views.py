# -*- coding: utf-8 -*-

import random

from django.core.urlresolvers import reverse
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from django.views.generic import DetailView, ListView
from django.template import RequestContext
from django.http import HttpResponseRedirect

from wiki.models import Article, ModifyHistory


class WikiHome(ListView):
    model = Article
    template_name = 'wiki/home.html'

class WikiContent(DetailView):
    model = Article
    template_name = 'wiki/article.html'

class WikiHistory(ListView):
    model = ModifyHistory
    template_name = 'wiki/history.html'

@login_required(login_url='/accounts/login/')
def modify_article(request, pk):
    article = Article.objects.filter(title=pk)
    if article:
        content = article[0].content
    else:
        content = ''

    return render_to_response('wiki/modify.html', {'title': pk, 'content': content}, context_instance=RequestContext(request))

def find_article(request, pk):
    article = Article.objects.filter(title=pk)
    if article:
        return render_to_response('wiki/article.html', {'article': article[0]}, context_instance=RequestContext(request))
    else:
        return render_to_response('wiki/notfound.html', {'title': pk}, context_instance=RequestContext(request))

def show_random(request):
    random_idx = random.randint(0, Article.objects.count() - 1)
    random_obj = Article.objects.all()[random_idx]
    return HttpResponseRedirect(reverse('wikiarticle', kwargs={'pk': random_obj.title}))

def show_history(request, pk):
    history = ModifyHistory.objects.filter(title=pk)
    return render_to_response('wiki/history.html', {'object_list': history}, context_instance=RequestContext(request))

def show_history_detail(request, pk):
    obj = ModifyHistory.objects.filter(code=pk)
    diff = obj[0].diff.split('\n')
    return render_to_response('wiki/history_detail.html', {'title': obj[0].title, 'diff': diff}, context_instance=RequestContext(request))