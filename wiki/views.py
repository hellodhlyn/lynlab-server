# coding=utf-8
from django.core.exceptions import ObjectDoesNotExist
from django.http import Http404

from .models import Article
from django.shortcuts import render, redirect


def article(request, title):
    try:
        article_instance = Article.objects.get(title=title)
    except ObjectDoesNotExist:
        raise Http404

    # 로그인이 필요할 경우에 대한 확인
    if not article_instance.is_public and not request.user.is_authenticated():
        return redirect('/accounts/login/?next=%s' % request.path)

    context = {
        'article': article_instance
    }
    return render(request, 'wiki/article.html', context=context)
