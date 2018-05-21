import magic
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import pre_save, pre_delete
from django.dispatch import receiver


class Object(models.Model):
    """
    스토리지 파일
    """

    file_obj = models.FileField()
    content_type = models.CharField(max_length=200, default='text')

    name = models.CharField(max_length=200, unique=True)
    uploader = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    safety_checked = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)


@receiver(pre_save, sender=Object)
def pre_object_save(sender, instance, *args, **kwargs):
    instance.content_type = magic.from_buffer(instance.file_obj.read(1024), mime=True)


@receiver(pre_delete, sender=Object)
def pre_object_delete(sender, instance, *args, **kwargs):
    instance.file_obj.delete(save=False)
