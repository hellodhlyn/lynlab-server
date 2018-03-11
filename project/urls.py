from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sitemaps import GenericSitemap
from django.contrib.sitemaps.views import sitemap
from django.views.generic import TemplateView, RedirectView

import blog.admin as blog_admin
import blog.models as blog
import blog.views as blog_view
import dashboard.views as dashboard_view
import moneybook.views as moneybook_view
import storage.views as storage_view
import wiki.services as wiki_service
import wiki.views as wiki_view
from media.views import show_media

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
    url(r'^resume/$', TemplateView.as_view(template_name='resume.html'), name='resume'),
    url(r'^about/$', RedirectView.as_view(pattern_name='resume', permanent=True)),

    # blog:
    url(r'^blog/$', blog_view.index, name='blog'),
    url(r'^blog/myadmin/$', blog_admin.admin, name='blogadmin'),
    url(r'^blog/myadmin/create/tweet/$', blog_admin.create_tweet, name='blog-admin-create-tweet'),
    url(r'^blog/myadmin/modify/$', blog_admin.create_post, name='blog-admin-create-post'),
    url(r'^blog/myadmin/modify/(?P<pk>\d+)$', blog_admin.modify_post, name='blog-admin-modify-post'),
    url(r'^blog/myadmin/series/$', blog_admin.series, name='blog-admin-create-series'),
    url(r'^blog/myadmin/series/modify/(?P<id>\d+)/$', blog_admin.modify_series, name='blog-admin-modify-series'),
    url(r'^blog/(?P<pk>\d+)/$', blog_view.post, name='detail'),

    # dashboard:
    url(r'^dashboard/$', dashboard_view.dashboard, name='dashboard'),
    url(r'^dashboard/bus$', dashboard_view.bus, name='dashboard-bus'),

    # wiki:
    url(r'^wiki/$', wiki_view.welcome, name='wiki'),
    url(r'^wiki/search/$', wiki_service.search_document, name='wiki-search'),
    url(r'^wiki/search/(?P<title>[\w|\W]+)/$', wiki_view.suggest_document, name='wiki-document-suggest'),
    url(r'^wiki/modify/(?P<title>[\w|\W]+)/$', wiki_view.modify_document, name='wiki-document-modify'),
    url(r'^wiki/history/(?P<title>[\w|\W]+)/$', wiki_view.list_revisions, name='wiki-document-history'),
    url(r'^wiki/history/$', wiki_view.list_revisions, name='wiki-history'),
    url(r'^wiki/(?P<title>[\w|\W]+)/$', wiki_view.get_document, name='wiki-document'),

    # media:
    url(r'^media/(?P<pk>[\w|\W]+)/$', show_media, name='mediashow'),

    # moneybook:
    url(r'^moneybook/$', moneybook_view.main, name='moneybook'),
    url(r'^moneybook/(?P<year>\d+)/(?P<month>\d+)/$', moneybook_view.by_year_month, name='moneybook-year-month'),
    url(r'^moneybook/modify/(?P<transaction_id>[\w|\W]+)/$', moneybook_view.modify, name='moneybook-modify'),

    # storage
    url(r'^storage/$', storage_view.index, name='storage'),
    url(r'^storage/recent/$', storage_view.recent, name='storage-recent'),
    url(r'^storage/upload/$', storage_view.upload, name='storage-upload'),
    url(r'^storage/delete/(?P<name>[\w|\W]+)/$', storage_view.delete, name='storage-delete'),
    url(r'^storage/(?P<name>[\w|\W]+)/$', storage_view.show, name='storage-show'),

    # admin:
    url(r'^admin/', admin.site.urls),

    # member:
    # url(r'^accounts/', include('django.contrib.auth.urls')),
    url(r'^accounts/', include('registration.backends.hmac.urls')),

    # static:
    url(r'^robots.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name='robots'),
    url(r'^sitemap\.xml$', sitemap, sitemaps, name='django.contrib.sitemaps.views.sitemap'),
]
