from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class Reservation(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(blank=False, null=True, unique=True)
    qty = models.IntegerField(default=8)
    # place = models.ForeignKey(Place)
    status = models.CharField(max_length=1, default='N')
    value = models.FloatField(null=True, blank=True)
    reservation_date = models.DateTimeField(auto_now=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    payment_confirmation = models.CharField(null=True, blank=True, max_length=200)

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
        self.status='P'
        self.payment_confirmation=unicode(confirmation)
        self.payment_date=datetime.now()
        self.save()

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
            if reservation.status=='P' or reservation.reservation_date >= now - timedelta(days=1):
                print "{0} - {1}".format(reservation.pk, reservation_id)
                if reservation.pk != reservation_id:
                    occupied.append(reservation.date.strftime("%Y-%m-%d"))
        return occupied
