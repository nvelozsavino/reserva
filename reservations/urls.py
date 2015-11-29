# -*- coding: utf-8 *-*
from django.conf.urls import patterns, url

urlpatterns = patterns('reservations.views',
    url('^$', 'index',name='reservations_index'),
    url('^new$', 'edit',name='reservations_new'),
    url('^payment$', 'payment',name='reservations_payment'),
    url('^payment/(?P<reservation_id>(\d+))/$', 'payment',name='reservation_payment'),
    url('^success/(?P<reservation_id>(\d+))/$', 'payment_success',name='payment_success'),
    url('^info/(?P<reservation_id>(\d+))/$', 'info',name='reservation_info'),
    url('^edit/(?P<reservation_id>(\d+))/$', 'edit', name='reservation_edit'),
    url('^delete/(?P<reservation_id>(\d+))/$', 'delete', name='reservation_delete'),
    url('^getdates/(?P<reservation_id>(\d+))/$','get_reserved_dates',name='reservation_get_reserved_dates'),
    url('^cancel_pending/$','cancel_pending_reservations',name='reservation_cancel_pending')

)
