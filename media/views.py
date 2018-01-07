from django.http import HttpResponse
from django.urls import Resolver404

from .models import Media


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
