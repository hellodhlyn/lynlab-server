# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView
from django.http import HttpResponse

from wiki.views import WikiHome, WikiContent, find_article, modify_article, \
	show_history_all, show_history, show_random, show_history_detail
from media.views import upload_view, show_media

import blog.views as BlogView
import blog.admin as BlogAdmin

import blog.models as blog
import wiki.models as wiki
import media.models as media

urlpatterns = [
	# global:
	url(r'^$', RedirectView.as_view(url='blog/')),
	url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

	# blog:
	url(r'^blog/$', BlogView.show_posts, name='home'),
	url(r'^blog/myadmin/$', BlogAdmin.admin, name='blogadmin'),
	url(r'^blog/myadmin/create/tweet/$', BlogAdmin.create_tweet, name='blogadmincreatetweet'),
	# url(r'^blog/myadmin/modify/(?P<pk>\d+)$', BlogView.admin_modify, name='blogadmin'),
	url(r'^blog/(?P<pk>\d+)/$', BlogView.PostDetail.as_view(), name='detail'),
	# url(r'^blog/', include('blog.urls')),

	# wiki:
	url(r'^wiki/$', WikiHome.as_view(), name='wiki'),
	url(r'^wiki/random/$', show_random, name='wikirandom'),
	url(r'^wiki/history/$', show_history_all, name='wikihistory'),
	url(r'^wiki/history/(?P<pk>[\w|\W]+)/$', show_history_detail, name='wikihistorydetail'),
	url(r'^wiki/(?P<pk>[\w|\W]+)/modify/$', modify_article, name='wikimodify'),
	url(r'^wiki/(?P<pk>[\w|\W]+)/history/$', show_history, name='wikiarticlehistory'),
	url(r'^wiki/(?P<pk>[\w|\W]+)/$', find_article, name='wikiarticle'),

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
	url(r'^v1/wiki/search/$', wiki.search, name='api_wikisearch'),
	url(r'^v1/wiki/modify/$', wiki.modify, name='api_wikimodify'),
	url(r'^v1/media/upload/$', media.upload, name='api_mediaupload'),

	url(r'^oauth/twitter/', include('twython_django_oauth.urls')),

	# static:
]
