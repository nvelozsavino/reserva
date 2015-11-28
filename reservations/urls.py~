# -*- coding: utf-8 *-*
from django.conf.urls import patterns, url

urlpatterns = patterns('reservations.views',
    url('^$', 'index',name='reservations_index'),
    url('^new$', 'new',name='reservations_new'),
    url('^payment$', 'payment',name='reservations_payment'),
    url('^payment/(?P<reservation_id>(\d+))/$', 'payment',name='reservation_payment'),
    url('^getdates/$','getreserveddates',name='reservation_getreserveddates')

)
