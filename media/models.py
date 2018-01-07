from django.db import models


class Media(models.Model):
    class Meta:
        verbose_name = u'media'

    title = models.CharField(verbose_name=u'title', max_length=64)
    uploader = models.CharField(verbose_name=u'uploader', max_length=64)
    uploaded = models.DateTimeField(auto_now_add=True)
