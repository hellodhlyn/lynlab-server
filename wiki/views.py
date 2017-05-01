# coding=utf-8
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.http import Http404
from django.shortcuts import render, redirect

from .models import Document, DocumentPermission


class LoginRequired(Exception):
    pass


def _get_document_item(request, title):
    """
    문서를 가져온다.
    :param request: 
    :return: 
    """
    document = Document.objects.get(title=title)

    # 로그인이 필요할 경우에 대한 확인
    if document.permission == DocumentPermission.ADMIN_USER and not request.user.is_staff():
        raise Http404
    elif document.permission == DocumentPermission.LOGIN_USER and not request.user.is_authenticated():
        raise LoginRequired

    return document


def get_document(request, title):
    """
    문서 보기
    """
    try:
        document = _get_document_item(request, title)
    except LoginRequired:
        return redirect('/accounts/login/?next=%s' % request.path)
    except ObjectDoesNotExist:
        return redirect(reverse('wiki-document-suggest', kwargs={'title': title}))

    context = {'document': document}
    return render(request, 'wiki/document.html', context=context)


@login_required(login_url='/accounts/login/')
def modify_document(request, title):
    """
    문서 편집
    """
    if request.method == "GET":
        try:
            document = _get_document_item(request, title)
        except LoginRequired:
            return redirect('/accounts/login/?next=%s' % request.path)
        except ObjectDoesNotExist:
            raise Http404

        context = {'document': document}
        return render(request, 'wiki/modify.html', context=context)

    elif request.method == "POST":
        try:
            document = _get_document_item(request, title)
        except (LoginRequired, ObjectDoesNotExist):
            return render(request, "400.html", status=400)

        document.content = request.POST['content']
        document.save()

        return redirect(reverse('wiki-document', kwargs={'title': document.title}))


def suggest_document(request, title):
    """
    문서 제안
    """
    suggests = Document.objects.filter(title__icontains=title).order_by('title')

    context = {
        'title': title,
        'suggests': suggests
    }
    return render(request, 'wiki/suggest.html', context=context)
