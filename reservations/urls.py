# -*- coding: utf-8 *-*
from django.conf.urls import patterns, url,include

urlpatterns = patterns('reservations.views',
    url('^$', 'index',name='index'),
    url('^reservation_list$', 'reservation_list',name='reservations_list'),
    url('^new$', 'edit',name='reservations_new'),
    url('^payment$', 'payment',name='reservations_payment'),
    url('^payment/(?P<reservation_id>(\d+))/$', 'payment',name='reservation_payment'),
    url('^success/(?P<reservation_id>(\d+))/$', 'payment_success',name='payment_success'),
    url('^info/(?P<reservation_id>(\d+))/$', 'info',name='reservation_info'),
    url('^edit/(?P<reservation_id>(\d+))/$', 'edit', name='reservation_edit'),
    url('^delete/(?P<reservation_id>(\d+))/$', 'delete', name='reservation_delete'),
    url('^getdates/(?P<reservation_id>(\d+))/$','get_reserved_dates',name='reservation_get_reserved_dates'),
    url('^cancel_pending/$','cancel_pending_reservations',name='reservation_cancel_pending'),
    url(r'^payment/paypal/', include('paypal.standard.ipn.urls')),
    # url('^payment/ipn/','paypal_ipn', name='paypal_ipn'),
    url('^payment/return/','paypal_return', name='paypal_return'),
    url('^payment/cancel/','paypal_cancel_return', name='paypal_cancel_return'),
    # url('^login$','login_user', name='login'),
    # url('^logout$', 'logout_user', name='logout')


)
