from django.conf.urls import patterns, include, url
from django.contrib import admin
from records import views as record_views
urlpatterns = patterns('',
	url(r'^$', record_views.home_page, name='home'),
	url(r'^records/', include('records.urls')),
	url(r'^artists/(\d+)/$',record_views.view_artist,name='view_artist'),
	url(r'^artists/new$',record_views.new_artist,name='new_artist'),
	url(r'^admin/', include(admin.site.urls)),
	url(r'^accounts/', include('accounts.urls')),
)
