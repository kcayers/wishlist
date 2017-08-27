from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^dashboard$', views.home),
    url(r'^wish_item$', views.wish_item),
    url(r'^create$', views.create),
    url(r'^wish_item/(?P<item_id>\d+)$', views.show_item),
    url(r'^add/(?P<item_id>\d+)$',views.add),
    url(r'^remove/(?P<item_id>\d+)$', views.remove),
    url(r'^delete/(?P<item_id>\d+)$', views.delete),
    url(r'^logout$', views.logout),
]
