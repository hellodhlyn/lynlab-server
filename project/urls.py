# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import RedirectView, TemplateView
from django.http import HttpResponse

from media.views import upload_view, show_media

import blog.admin as BlogAdmin
import blog.models as blog
import blog.views as BlogView
import blog.controllers as BlogControl

import media.models as media

import simple_wiki.models as WikiModel

sitemaps = {
	'sitemaps': {
		'blog': GenericSitemap({
			'queryset': blog.Post.objects.all(),
			'date_field': 'created',
		}, changefreq='monthly'),
		'wiki': GenericSitemap({
			'queryset': WikiModel.Article.objects.all(),
			'date_field': 'created',
		}, changefreq='weekly'),
	},
}

urlpatterns = [
	# global:
	url(r'^$', TemplateView.as_view(template_name='welcome.html'), name='home'),
	url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

	# blog:
	url(r'^blog/$', BlogView.main, name='blog'),
	url(r'^blog/myadmin/$', BlogAdmin.admin, name='blogadmin'),
	url(r'^blog/myadmin/create/tweet/$', BlogAdmin.create_tweet, name='blogadmincreatetweet'),
	url(r'^blog/myadmin/modify/$', BlogAdmin.create_post, name='blogadmincreatepost'),
	url(r'^blog/myadmin/modify/(?P<pk>\d+)$', BlogAdmin.modify_post, name='blogadminmodifypost'),
	url(r'^blog/(?P<pk>\d+)/$', BlogView.post_detail, name='detail'),
	# url(r'^blog/', include('blog.urls')),

	# wiki:
	url(r'^wiki/', include('simple_wiki.urls')),

	# media: 
	url(r'^media/upload/$', upload_view, name='mediaupload'),
	url(r'^media/(?P<pk>[\w|\W]+)/$', show_media, name='mediashow'),

	# admin:
	url(r'^admin/', include(admin.site.urls)),

	# member:
	#url(r'^accounts/', include('django.contrib.auth.urls')),
	url(r'^accounts/profile/$', RedirectView.as_view(url='/wiki/')),
	url(r'^accounts/', include('registration.backends.hmac.urls')),

	# apis:
	url(r'^v1/blog/create/$', BlogControl.create, name='api_blogcreate'),
	url(r'^api/blog/posts/$', BlogControl.load_posts, name='api-blog-posts'),
	url(r'^v1/media/upload/$', media.upload, name='api_mediaupload'),

	# static:
	url(r'^robots.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
	url(r'^sitemap\.xml$', sitemap, sitemaps, name='django.contrib.sitemaps.views.sitemap'),
]
