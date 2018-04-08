import datetime

from django.db import models
from django.urls import reverse
from django.utils import translation
from django.utils.timezone import utc


class Category(models.Model):
    """
    Category of posts.
    """

    class Meta:
        verbose_name = u'category'
        ordering = ['name']

    name = models.CharField(verbose_name=u'name', max_length=50)
    url = models.CharField(max_length=32, default='')

    def __str__(self):
        return self.name


class PostType(models.Model):
    """
    Type of posts.
    """
    name = models.CharField(max_length=50)
    icon = models.CharField(max_length=50)
    default = models.BooleanField(default=True)


class Series(models.Model):
    """
    Series of the posts.
    """
    name = models.CharField(max_length=30, default='')

    def get_posts(self):
        return Post.objects.filter(series=self).order_by('-created')

    def post_num(self):
        return Post.objects.filter(series=self).count()


class Tag(models.Model):
    """
    Tag of posts.
    """
    url = models.CharField(max_length=20, null=False, default='')

    def get_name(self):
        try:
            return TagTranslations.objects.get(tag=self, language=translation.get_language())
        except:
            return self.url

    def __str__(self):
        return self.url


class TagTranslations(models.Model):
    """
    Translations of tags.
    """
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=False, default='')
    language = models.CharField(max_length=8, null=False)

    def __str__(self):
        return self.name


class Post(models.Model):
    """
    Post.
    """

    class Meta:
        verbose_name = u'post'
        ordering = ['created']

    # Meta infos
    category = models.ForeignKey(Category, null=True, blank=True, on_delete=models.DO_NOTHING)
    created = models.DateTimeField(auto_now_add=True)
    preview = models.CharField(null=True, blank=True, max_length=256)
    hitcount = models.IntegerField(default=0)
    series = models.ForeignKey(Series, related_name='posts', null=True, on_delete=models.DO_NOTHING)

    # Contents
    title = models.CharField(max_length=256)
    description = models.TextField(blank=True, default='')
    content = models.TextField(blank=True, default='')

    # Options
    public_post = models.BooleanField(default=False)

    def __str__(self):
        return self.title

    def is_recent_post(self):
        """
        :return: True if post written in a 24 hours. False otherwise.
        """
        if self.created:
            now = datetime.datetime.utcnow().replace(tzinfo=utc)
            timediff = now - self.created
            if timediff.total_seconds() < 86400:
                return True
            else:
                return False

    def get_tags(self):
        """
        :return: Tags of the post on a List object.
        """
        return map(lambda x: x.tag, PostTagRelation.objects.filter(post=self))

    def get_tags_url(self):
        """
        :return: Tags of the post on a comma separated string.
        """
        relations = PostTagRelation.objects.filter(post=self)
        return ','.join(map(str, map(lambda x: x.url, map(lambda y: y.tag, relations))))


class PostTypeRelation(models.Model):
    """
    Many-to-many relation table of Post and PostType
    """
    post_id = models.IntegerField()
    type_id = models.IntegerField()


class PostTagRelation(models.Model):
    """
    Many-to-many relation table of Post and Tag.
    """
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

