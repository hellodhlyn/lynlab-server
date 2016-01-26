# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView
from django.http import HttpResponse

from media.views import upload_view, show_media

import blog.views as BlogView
import blog.admin as BlogAdmin

import blog.models as blog
import media.models as media

urlpatterns = [
	# global:
	url(r'^$', RedirectView.as_view(url='blog/')),
	url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

	# blog:
	url(r'^blog/$', BlogView.show_posts, name='home'),
	url(r'^blog/myadmin/$', BlogAdmin.admin, name='blogadmin'),
	url(r'^blog/myadmin/create/tweet/$', BlogAdmin.create_tweet, name='blogadmincreatetweet'),
	url(r'^blog/myadmin/modify/$', BlogAdmin.create_post, name='blogadmincreatepost'),
	url(r'^blog/myadmin/modify/(?P<pk>\d+)$', BlogAdmin.modify_post, name='blogadminmodifypost'),
	url(r'^blog/(?P<pk>\d+)/$', BlogView.PostDetail.as_view(), name='detail'),
	# url(r'^blog/', include('blog.urls')),

	# wiki:
	url(r'^wiki/', include('simple-wiki.urls')),

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
	url(r'^v1/blog/create/$', blog.create, name='api_blogcreate'),
	url(r'^v1/media/upload/$', media.upload, name='api_mediaupload'),

	# static:
]
