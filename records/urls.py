from django.conf.urls import patterns,url
from . import views
urlpatterns = patterns('',
	url(r'^(\d+)/$',views.view_record,name='view_record'),
	url(r'^new$', views.new_record,name='new_record'),
)