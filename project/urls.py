# -*- coding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.views.generic import RedirectView, TemplateView
from django.http import HttpResponse

from blog.views import PostList, PostDetail, PostCreate
from wiki.views import WikiHome, WikiContent, WikiHistory, find_article, modify_article, show_history

import wiki.models as wiki

urlpatterns = patterns('',
	# global:
	url(r'^$', RedirectView.as_view(url='blog/')),
	url(r'^about/$', TemplateView.as_view(template_name='about.html'), name='about'),

	# blog:
	url(r'^blog/$', PostList.as_view(), name='home'),
	url(r'^blog/(?P<pk>\d+)/$', PostDetail.as_view(), name='detail'),
	url(r'^blog/create/$', PostCreate.as_view(), name='create'),
	# url(r'^blog/', include('blog.urls')),

	# wiki:
	url(r'^wiki/$', WikiHome.as_view(), name='wiki'),
	url(r'^wiki/history/$', WikiHistory.as_view(), name='wikihistory'),
	url(r'^wiki/(?P<pk>[\w|\W]+)/modify/$', modify_article, name='wikimodify'),
	url(r'^wiki/(?P<pk>[\w|\W]+)/history/$', show_history, name='wikiarticlehistory'),
	url(r'^wiki/(?P<pk>[\w|\W]+)/$', find_article, name='wikiarticle'),

	# admin:
	url(r'^admin/', include(admin.site.urls)),

	# member:
	#url(r'^accounts/', include('django.contrib.auth.urls')),
	url(r'^accounts/profile/$', RedirectView.as_view(url='/wiki/')),
	url(r'^accounts/', include('registration.backends.hmac.urls')),

	# apis:
	url(r'^v1/wiki/search/$', wiki.search),
	url(r'^v1/wiki/modify/$', wiki.modify),

	# static:
)
