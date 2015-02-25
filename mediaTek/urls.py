from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
	url(r'^$', 'records.views.home_page', name='home'),
	url(r'^records/', include('records.urls')),
    url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/', include('accounts.urls')),
)
