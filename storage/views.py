import datetime
import mimetypes

from django import urls
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotFound, \
    HttpResponseForbidden, HttpResponseNotAllowed
from django.shortcuts import render, redirect
from django.urls import reverse

from storage.forms import ObjectForm
from storage.models import Object


def index(request):
    if request.method == 'GET':
        cursor = request.GET.get('cursor', datetime.datetime.now())
        context = {
            'total_count': Object.objects.count(),
            'files': Object.objects.filter(modified_at__lt=cursor).order_by('-created_at'),
            'navbar': _navigation()
        }

        return render(request, 'index.html', context=context)


def upload(request):
    """
    Upload an object to server.
    """
    if request.method == 'GET':
        form = ObjectForm()
    elif request.method == 'POST':
        form = ObjectForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            # Make object and save
            obj = Object(file=request.FILES['file'],
                         name=request.POST['name'],
                         uploader=request.user.username)
            try:
                with transaction.atomic():
                    obj.save()
                messages.add_message(request, level=messages.SUCCESS, message='성공적으로 업로드 되었습니다.')
                return redirect(urls.reverse('storage'))
            except IntegrityError:
                form.add_error('name', '파일 이름이 유효하지 않습니다. 다른 이름으로 다시 시도해주세요.')

        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    context = {
        'form': form,
        'navbar': _navigation()
    }

    return render(request, 'upload.html', context=context)


def show(request, name):
    """
    Get an object.
    """
    if request.method == 'GET':
        try:
            obj = Object.objects.get(name=name)

            # TODO: Block if safety check is not finished
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        return HttpResponse(obj.file.read(), content_type=obj.content_type)


def delete(request, name):
    """
    Delete an object.
    """
    if request.method == 'GET':
        try:
            obj = Object.objects.get(name=name)
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        if not obj.uploader == request.user.username:
            return HttpResponseForbidden()

        obj.delete()

        messages.add_message(request, level=messages.SUCCESS, message='성공적으로 삭제되었습니다.')
        return redirect(reverse('storage'))


def _navigation():
    return {
        'title': {'name': 'LYnStorage', 'url': 'storage'},
        'left': [
            {'name': '업로드', 'url': 'storage-upload'},
        ],
        'right': [
            {
                'name': 'LYnLab',
                'dropdown': True,
                'submenu': [
                    {'name': '블로그', 'url': 'blog'},
                    {'name': '위키', 'url': 'wiki'},
                    {'outer_url': True, 'name': '앉아서 집에가자', 'url': 'https://bus.lynlab.co.kr'}
                ]
            },
        ],
    }
