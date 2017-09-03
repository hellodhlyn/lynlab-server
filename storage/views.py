import datetime

from django import urls
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction, IntegrityError
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse, HttpResponseNotAllowed
from django.shortcuts import render, redirect

from storage.apps import navigation
from storage.forms import ObjectForm
from storage.models import Object


def index(request):
    if request.method == 'GET':
        cursor = request.GET.get('cursor', datetime.datetime.now())
        context = {
            'total_count': Object.objects.count(),
            'files': Object.objects.filter(modified_at__lt=cursor).order_by('-created_at'),
            'navbar': navigation()
        }

        return render(request, 'index.html', context=context)


def upload(request):
    if request.method == 'GET':
        form = ObjectForm()
    elif request.method == 'POST':
        form = ObjectForm(data=request.POST, files=request.FILES)

        if form.is_valid():
            obj = Object(file=request.FILES['file'],
                         name=request.POST['name'],
                         uploader=request.user.username)

            try:
                with transaction.atomic():
                    # TODO: Safety check
                    obj.save()
                return redirect(urls.reverse('storage'))
            except IntegrityError:
                form.add_error('name', '파일 이름이 유효하지 않습니다. 다른 이름으로 다시 시도해주세요.')

        else:
            return HttpResponseBadRequest()
    else:
        return HttpResponseNotAllowed(['GET', 'POST'])

    context = {
        'form': form,
        'navbar': navigation()
    }

    return render(request, 'upload.html', context=context)


def show(request, name):
    if request.method == 'GET':
        try:
            obj = Object.objects.get(name=name)

            # TODO: Block if safety check is not finished
        except ObjectDoesNotExist:
            return HttpResponseNotFound()

        return HttpResponse(obj.file.read(), content_type=obj.content_type)
