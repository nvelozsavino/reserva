# -*- coding: utf-8 *-*
from django.conf.urls import patterns, url

urlpatterns = patterns('reservations.views',
    url('^$', 'index',name='reservations_index'),
    url('^new$', 'new',name='reservations_new'),
    url('^payment$', 'payment',name='reservations_payment'),
    url('^payment/(?P<reservation_id>(\d+))/$', 'payment',name='reservation_payment'),
    url('^success/(?P<reservation_id>(\d+))/$', 'payment_success',name='payment_success'),
    url('^info/(?P<reservation_id>(\d+))/$', 'info',name='reservation_info'),
    url('^edit/(?P<reservation_id>(\d+))/$', 'edit', name='reservation_edit'),
    url('^delete/(?P<reservation_id>(\d+))/$', 'delete', name='reservation_delete'),
    url('^getdates/(?P<reservation_id>(\d+))/$','getreserveddates',name='reservation_getreserveddates')

)
