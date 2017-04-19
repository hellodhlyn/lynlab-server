from django.shortcuts import render


def error_410(request):
    """
    410 Gone
    """
    return render(request, "410.html", status=410)
