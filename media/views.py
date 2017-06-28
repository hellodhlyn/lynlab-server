from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import Resolver404
from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext

from .models import Media


@login_required(login_url='/accounts/login/')
def upload_view(request):
    template_name = 'media/upload.html'
    context = {}

    return render_to_response(template_name, context, context_instance=RequestContext(request))


def show_media(request, pk):
    res_file = Media.objects.filter(title=pk)

    if not res_file:
        raise Resolver404
    else:
        req_directory = u'media/storage/' + res_file[0].title
        req_directory = req_directory.encode('utf8', 'replace')
        with open(req_directory, "rb") as f:
            response = HttpResponse(f.read(), content_type="image")

    return response
