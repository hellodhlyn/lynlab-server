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

@login_required(login_url='/accounts/login/')
def modify_article(request, pk):
    article = Article.objects.filter(title=pk)
    if article:
        content = article[0].content
        code = article[0].code
    else:
        content = ''
        code = ''

    return render_to_response('wiki/modify.html', {'title': pk, 'content': content, 'code': code}, context_instance=RequestContext(request))

def find_article(request, pk):
    article = Article.objects.filter(title=pk)
    if article:
        if article[0].code == 303:
            article = Article.objects.filter(title=article[0].content)
            return render_to_response('wiki/article.html', {'article': article[0], 'redirect_origin': pk}, context_instance=RequestContext(request))
        else:
            return render_to_response('wiki/article.html', {'article': article[0]}, context_instance=RequestContext(request))
    else:
        return render_to_response('wiki/notfound.html', {'title': pk}, context_instance=RequestContext(request))

def show_random(request):
    random_idx = random.randint(0, Article.objects.count() - 1)
    random_obj = Article.objects.all()[random_idx]
    return HttpResponseRedirect(reverse('wikiarticle', kwargs={'pk': random_obj.title}))

def show_history_all(request):
    template_name = 'wiki/history.html'
    paged_template_name = 'wiki/history_paged.html'

    context = {
        'object_list': ModifyHistory.objects.all().order_by('-timestamp'),
        'page_template': paged_template_name
    }

    if request.is_ajax():
        template_name = paged_template_name

    return render_to_response(template_name, context, context_instance=RequestContext(request))

def show_history(request, pk):
    template_name = 'wiki/history.html'
    paged_template_name = 'wiki/history_paged.html'

    context = {
        'object_list': ModifyHistory.objects.filter(title=pk),
        'page_template': paged_template_name
    }

    if request.is_ajax():
        template_name = paged_template_name

    return render_to_response(template_name, context, context_instance=RequestContext(request))

def show_history_detail(request, pk):
    obj = ModifyHistory.objects.filter(code=pk)
    diff = obj[0].diff.split('\n')
    return render_to_response('wiki/history_detail.html', {'title': obj[0].title, 'diff': diff}, context_instance=RequestContext(request))