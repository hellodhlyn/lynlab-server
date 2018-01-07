from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, PermissionDenied
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse

from .models import Document, DocumentPermission, DocumentRevision


class LoginRequired(Exception):
    def __init__(self, permission):
        self.permission = permission


def welcome(request):
    context = {'document_count': Document.objects.count()}
    return render(request, 'wiki/welcome.html', context)


def _get_document_item(request, title):
    """
    문서를 가져온다.
    :param request: 
    :return: 
    """
    document = Document.objects.get(title=title)

    # 로그인이 필요할 경우에 대한 확인
    if document.permission == DocumentPermission.ADMIN_USER.value:
        if not request.user.is_authenticated:
            raise LoginRequired(document.permission)
        if not request.user.is_staff:
            raise PermissionDenied
    elif document.permission == DocumentPermission.LOGIN_USER.value and not request.user.is_authenticated:
        raise LoginRequired(document.permission)

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
        return suggest_document(request, title)

    context = {'document': document}
    return render(request, 'wiki/document.html', context=context)


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


@login_required(login_url='/accounts/login/')
def modify_document(request, title):
    """
    문서 편집
    """
    if request.method == "GET":
        try:
            document = _get_document_item(request, title)
        except ObjectDoesNotExist:
            document = Document(title=title)
        except LoginRequired:
            return redirect('/accounts/login/?next=%s' % request.path)

        context = {'document': document}
        return render(request, 'wiki/modify.html', context=context)

    elif request.method == "POST":
        # 문서 저장
        try:
            document = _get_document_item(request, title)
        except ObjectDoesNotExist:
            document = Document(title=title)
        except LoginRequired:
            raise PermissionDenied

        document.content = request.POST['content']
        document.permission = DocumentPermission(int(request.POST['permission'])).value
        document.save()

        # Revision 생성
        revision_num = DocumentRevision.objects.filter(document=document).count() + 1
        revision = DocumentRevision(document=document,
                                    revision=revision_num,
                                    editor=request.user.username)
        revision.save()

        return redirect(reverse('wiki-document', kwargs={'title': document.title}))


def list_revisions(request, title=None):
    """
    문서 편집 역사
    """
    if title:
        try:
            document = _get_document_item(request, title)
        except ObjectDoesNotExist:
            raise Http404
        except LoginRequired:
            return redirect('/accounts/login/?next=%s' % request.path)

        revisions = DocumentRevision.objects.filter(document=document).order_by('-timestamp')
    else:
        document = None
        revisions = DocumentRevision.objects.all().order_by('-timestamp')

    context = {
        'document': document,
        'revisions': revisions
    }

    return render(request, 'wiki/history.html', context=context)
