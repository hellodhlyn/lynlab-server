# -*- coding: utf-8 -*-

from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView

import blog.admin as BlogAdmin
import blog.controllers as BlogControl
import blog.models as blog
import blog.views as BlogView
import dashboard.views as DashboardView
import media.models as media
from media.views import upload_view, show_media
import wiki.views as WikiView

sitemaps = {
    'sitemaps': {
        'blog': GenericSitemap({
            'queryset': blog.Post.objects.filter(public_post=True),
            'date_field': 'created',
        }, changefreq='monthly')
    },
}

urlpatterns = [
    # global:
    url(r'^$', TemplateView.as_view(template_name='welcome.html'), name='home'),
    url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

    # blog:
    url(r'^blog/$', BlogView.main, name='blog'),
    url(r'^blog/tag/(?P<tag>[\w|\W]+)/$', BlogView.by_tag, name='blog-tag'),
    url(r'^blog/category/(?P<category>[\w|\W]+)/$', BlogView.by_category, name='blog-category'),
    url(r'^blog/myadmin/$', BlogAdmin.admin, name='blogadmin'),
    url(r'^blog/myadmin/create/tweet/$', BlogAdmin.create_tweet, name='blog-admin-create-tweet'),
    url(r'^blog/myadmin/modify/$', BlogAdmin.create_post, name='blog-admin-create-post'),
    url(r'^blog/myadmin/modify/(?P<pk>\d+)$', BlogAdmin.modify_post, name='blog-admin-modify-post'),
    url(r'^blog/myadmin/series/$', BlogAdmin.series, name='blog-admin-create-series'),
    url(r'^blog/myadmin/series/modify/(?P<id>\d+)/$', BlogAdmin.modify_series, name='blog-admin-modify-series'),
    url(r'^blog/(?P<pk>\d+)/$', BlogView.post_detail, name='detail'),
    # url(r'^blog/', include('blog.urls')),

    # dashboard:
    url(r'^dashboard/$', DashboardView.dashboard, name='dashboard'),
    url(r'^dashboard/bus$', DashboardView.bus, name='dashboard-bus'),

    # wiki:
    url(r'^wiki/$', TemplateView.as_view(template_name='204.html')),
    url(r'^wiki/(?P<title>[\w|\W]+)/$', WikiView.article, name='wiki-article'),

    # media:
    url(r'^media/upload/$', upload_view, name='mediaupload'),
    url(r'^media/(?P<pk>[\w|\W]+)/$', show_media, name='mediashow'),

    # admin:
    url(r'^admin/', include(admin.site.urls)),

    # member:
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),

    # apis:
    url(r'^api/blog/posts/$', BlogControl.load_posts, name='api-blog-posts'),
    url(r'^api/blog/like/(?P<id>\d+)/$', BlogControl.like_post, name='api-blog-like-post'),
    url(r'^api/blog/unlike/(?P<id>\d+)/$', BlogControl.unlike_post, name='api-blog-unlike-post'),
    url(r'^v1/media/upload/$', media.upload, name='api_mediaupload'),

    # static:
    url(r'^robots.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    url(r'^sitemap\.xml$', sitemap, sitemaps, name='django.contrib.sitemaps.views.sitemap'),
]
