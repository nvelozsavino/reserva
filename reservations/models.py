# -*- coding: utf-8 *-*
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from utils import send_html_email
from django.core.validators import MaxValueValidator, MinValueValidator
import json

class Reservation(models.Model):
    RESERVATION_STATUS_CHOICES = (
        ('N', u'Pendiente'),
        ('P', u'Pagado'),
        ('C', u'Cancelado'),
    )

    RESERVATION_CURRENCY_CHOICES = (
        ('USD',u'USD'),
    )

    RESERVATION_CURRENCY='USD'

    RESERVATION_QTY_CUT = 8
    RESERVATION_BASE_PRICE = 2000

    RESERVATION_EXTRA_PRICE = 250
    RESERVATION_MAX_QTY=12
    RESERVATION_MIN_QTY=1


    

    user = models.ForeignKey(User, verbose_name=u'Usuario')
    date = models.DateField(blank=False, null=True, unique=True, verbose_name=u'Fecha del viaje')
    qty = models.IntegerField(default=RESERVATION_QTY_CUT, verbose_name=u'Cantidad de personas',validators=[MaxValueValidator(12),MinValueValidator(1)])
    # place = models.ForeignKey(Place)
    status = models.CharField(max_length=1, choices=RESERVATION_STATUS_CHOICES, default='N', verbose_name=u'Status')
    value = models.FloatField(null=True, blank=True, verbose_name=u'Precio')
    reservation_date = models.DateTimeField(auto_now=True, verbose_name=u'Fecha de creación')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name=u'Fecha del pago')
    payment_confirmation = models.CharField(null=True, blank=True, max_length=255, verbose_name=u'Confirmación de pago')

    qty_cut = models.IntegerField(default=RESERVATION_QTY_CUT, verbose_name=u'Cantidad mínima de personas')
    base_price = models.FloatField(default=RESERVATION_BASE_PRICE, verbose_name=u'Precio mínimo')
    extra_price = models.FloatField(default=RESERVATION_EXTRA_PRICE, verbose_name=u'Precio extra')
    currency = models.CharField(max_length=3, choices=RESERVATION_CURRENCY_CHOICES, default=RESERVATION_CURRENCY, verbose_name=u'Moneda')


    def __unicode__(self):
        return unicode(self.user.get_full_name()) + " (" + unicode(self.date) + ") - " + unicode(self.qty)

    def is_paid(self):
        if self.status=='P':
            return True
        return False

    def is_cancelled(self):
        if self.status=='C':
            return True
        return False

    def is_pending(self):
        if self.status=='N':
            return True
        return False

    def has_extra(self):
        if self.qty>self.qty_cut:
            return True
        return False

    def qty_dif(self):
        if self.has_extra:
            return self.qty-self.qty_cut
        return 0

    def price_dif(self):
        return (self.qty_dif() * self.extra_price)

    def save(self, *args, **kwargs): 
        if self.status != 'P':
            if self.qty<Reservation.RESERVATION_MIN_QTY:
                self.qty=Reservation.RESERVATION_MIN_QTY
            if self.qty>Reservation.RESERVATION_MAX_QTY:
                self.qty=Reservation.RESERVATION_MAX_QTY
            
            if self.qty<=self.qty_cut:
                self.value=self.base_price
            else:
                self.value=self.base_price+(self.extra_price*(self.qty-self.qty_cut))
        super(Reservation, self).save(*args, **kwargs)

    def pay(self, confirmation):
        if self.status != 'N':
            return False
        self.status='P'
        self.payment_confirmation=confirmation
        self.payment_date=datetime.now()
        self.save()
        self.send_payment_mail()
        return True

    def cancel(self):
        if self.status != 'N':
            return False
        self.status = 'C'
        self.save()
        self.send_cancel_mail()
        return True

    def send_payment_mail(self):
        subject = u'Payment Success ' + unicode (self.date)
        from_email = 'no-reply@pocotopocopo.com'
        to = [self.user.email]
        template = 'email/payment_confirmation.html'
        payment_info = json.loads(self.payment_confirmation)
        data = {'reservation': self, 'card': payment_info['source']['brand'], 'last4':payment_info['source']['last4'] }
        send_html_email(subject, from_email, to, template, data)

    def send_cancel_mail(self):
        subject = u'Reservation Cancelled ' + unicode(self.date)
        from_email = 'no-reply@pocotopocopo.com'
        to = [self.user.email]
        template = 'email/cancelation.html'
        data = {'reservation':self,}
        send_html_email(subject, from_email, to, template, data)



    @staticmethod
    def get_ocuped_dates(reservation_id=0, until=0):
        now=datetime.now()
        if (until is 0):
            untilDate=now.replace(year=now.year+1)
        else:
            untilDate=until
        reservations = Reservation.objects.filter(date__gte=now, date__lte=untilDate)
        occupied = []
        for reservation in reservations:
            if reservation.is_paid() or reservation.reservation_date > now - timedelta(days=1,seconds=3600):
                if reservation.pk != reservation_id:
                    occupied.append(reservation.date.strftime("%Y-%m-%d"))
        return occupied

    @staticmethod
    def cancel_pending_reservations(user=None):
        expired_time=datetime.now()-timedelta(days=1, seconds=3600)
        if user:
            pending_reservations = Reservation.objects.filter(user=user,reservation_date__lte=expired_time)
        else:
            pending_reservations = Reservation.objects.filter(reservation_date__lte=expired_time)
        cancelled = []
        for reservation in pending_reservations:
            result = reservation.cancel()
            cancelled.append((reservation, result))
        return cancelled


from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from base64 import b64decode
import re, sys

def process_payment(sender, **kwargs):
    print "Processing payment"
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Undertake some action depending upon `ipn_obj`.
        custom_code=b64decode(ipn_obj.custom)
        print "Custom Code: " + ipn_obj.custom + " decoded: " + custom_code
        m=re.search('reservation=(.*),(\d*)',custom_code)
        try:
            reservation_id= int(m.group(2))
            reservation=Reservation.objects().filter(pk=reservation_id)
            reservation.pay()
        except Reservation.DoesNotExist:
            print "not exist"
        except:
            print "otro error" + sys.exc_info()[0]


    else:
        print "fallo"


valid_ipn_received.connect(process_payment)
invalid_ipn_received.connect(process_payment)
