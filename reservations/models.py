# -*- coding: utf-8 *-*
from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User
from django.core.mail import send_mail
from utils import send_html_email

class Reservation(models.Model):
    RESERVATION_STATUS_CHOICES = (
        ('N', u'Pendiente'),
        ('P', u'Pagado'),
        ('C', u'Cancelado'),
    )
    user = models.ForeignKey(User, verbose_name=u'Usuario')
    date = models.DateField(blank=False, null=True, unique=True, verbose_name=u'Fecha del viaje')
    qty = models.IntegerField(default=8, verbose_name=u'Cantidad de personas')
    # place = models.ForeignKey(Place)
    status = models.CharField(max_length=1, choices=RESERVATION_STATUS_CHOICES, default='N', verbose_name=u'Status')
    value = models.FloatField(null=True, blank=True, verbose_name=u'Precio')
    reservation_date = models.DateTimeField(auto_now=True, verbose_name=u'Fecha de creación')
    payment_date = models.DateTimeField(null=True, blank=True, verbose_name=u'Fecha del pago')
    payment_confirmation = models.CharField(null=True, blank=True, max_length=200, verbose_name=u'Confirmación de pago')

    def __unicode__(self):
        return unicode(self.user.get_full_name()) + " (" + unicode(self.date) + ") - " + unicode(self.qty)

    def save(self, *args, **kwargs): 
        if self.status != 'P':
            if self.qty<=8:
                self.value=2000
            else:
                self.value=2000+(250*(self.qty-8))
        super(Reservation, self).save(*args, **kwargs)

    def pay(self, confirmation):
        if self.status != 'N':
            return False
        self.status='P'
        self.payment_confirmation=confirmation
        self.payment_date=datetime.now()
        self.send_payment_mail()
        self.save()
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
        to = self.user.email
        template = 'email/payment_confirmation.html'
        variables = {'reservation':self,}
        send_html_email(subject, from_email, to, template, variables)

    def send_cancel_mail(self):
        subject = u'Reservation Cancelled ' + unicode (self.date)
        from_email = 'no-reply@pocotopocopo.com'
        to = self.user.email
        template = 'email/cancelation.html'
        variables = {'reservation':self,}
        send_html_email(subject, from_email, to, template, variables)

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
            if reservation.status=='P' or reservation.reservation_date > now - timedelta(days=1,seconds=3600):
                print "{0} - {1}".format(reservation.pk, reservation_id)
                if reservation.pk != reservation_id:
                    occupied.append(reservation.date.strftime("%Y-%m-%d"))
        return occupied

    @staticmethod
    def cancel_pending_reservations():
        expired_time=datetime.now()-timedelta(days=1, seconds=3600)
        pending_reservations = Reservation.objects.filter(reservation_date__lte=expired_time)
        cancelled = []
        for reservation in pending_reservations:
            result = reservation.cancel()
            cancelled.append((reservation, result))
        return cancelled

