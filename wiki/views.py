# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.views.generic import DetailView, ListView
from django.shortcuts import render_to_response

from wiki.models import Article


class WikiHome(ListView):
	model = Article
	template_name = 'wiki/home.html'

class WikiContent(DetailView):
    model = Article
    template_name = 'wiki/article.html'

def find_by_title(request, pk):
    article = Article.objects.filter(title=pk)
    if article:
    	return render_to_response('wiki/article.html', {'article': article[0]})
    else:
    	return render_to_response('wiki/notfound.html', {'title': pk})