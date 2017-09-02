from django.db import models


class Object(models.Model):
    """
    스토리지 파일
    """

    file = models.FileField()
    content_type = models.CharField(max_length=200, default='text')

    name = models.CharField(max_length=200, unique=True)
    uploader = models.CharField(max_length=200)
    safety_checked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
