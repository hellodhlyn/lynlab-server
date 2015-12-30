from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import Resolver404
from django.http import HttpResponse, FileResponse
from django.shortcuts import render, render_to_response
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
        with open('media/storage/'+res_file[0].title, "rb") as f:
            response = HttpResponse(f.read(), content_type="image")
        #response = FileResponse(open(res_file[0].media.path))

    return response