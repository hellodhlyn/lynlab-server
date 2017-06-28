from django.db import models
from django.shortcuts import render_to_response
from django.template import RequestContext


class Media(models.Model):
    class Meta:
        verbose_name = u'media'

    title = models.CharField(verbose_name=u'title', max_length=64)
    uploader = models.CharField(verbose_name=u'uploader', max_length=64)
    uploaded = models.DateTimeField(auto_now_add=True)


def upload(request):
    if request.method == 'POST':
        status = is_valid(request)
        if status == 200:
            req_title = request.POST.get('title', False)
            req_directory = u'media/storage/' + req_title
            req_directory = req_directory.encode('utf8', 'replace')

            with open(req_directory, 'wb') as f:
                f.write(request.FILES['file'].read())

            instance = Media(title=req_title, uploader=request.user.username)
            instance.save()
            return render_to_response('media/upload_complete.html', {'title': req_title},
                                      context_instance=RequestContext(request))

    if status is None:
        status = 200

    return render_to_response('media/upload.html', {'error': status}, context_instance=RequestContext(request))


def is_valid(request):
    req_title = request.POST.get('title', False)

    if Media.objects.filter(title=req_title).count() is not 0:
        return 409

    return 200
