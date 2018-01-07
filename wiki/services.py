from django.shortcuts import redirect
from django.urls import reverse


def search_document(request):
    """
    문서 검색
    """
    title = request.POST['title']
    return redirect(reverse('wiki-document', kwargs={'title': title}))
