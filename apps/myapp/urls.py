from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^dash$', views.dash),
	url(r'^logout$', views.logout),
	url(r'^show/(?P<itemid>\d+)$', views.show),
	url(r'^create$', views.create),
	url(r'^new$', views.new),
	url(r'^join/(?P<itemid>\d+)$', views.join),
	url(r'^cancel/(?P<itemid>\d+)$', views.cancel),
	url(r'^delete/(?P<itemid>\d+)$', views.delete),
]
