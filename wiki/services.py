# -*- coding=utf-8 -*-
from django.core.urlresolvers import reverse
from django.shortcuts import redirect


def search_document(request):
    """
    문서 검색
    """
    title = request.POST['title']
    return redirect(reverse('wiki-document', kwargs={'title': title}))
