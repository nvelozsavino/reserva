from django.db import models
from datetime import datetime, timedelta
from django.contrib.auth.models import User


class Reservation(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(blank=True, null=True, unique=True)
    qty = models.IntegerField(default=8)
    # place = models.ForeignKey(Place)
    paid = models.BooleanField(default=False)
    reservation_date = models.DateTimeField(auto_now=True)
    payment_confirmation = models.CharField(null=True, blank=True, max_length=200)

    def __unicode__(self):
        return unicode(self.user.get_full_name()) + " (" + unicode(self.date) + ") - " + unicode(self.qty)

    @staticmethod
    def get_ocuped_dates(until=0):
        now=datetime.now()
        if (until is 0):
            untilDate=now.replace(year=now.year+1)
        else:
            untilDate=until
        reservations = Reservation.objects.filter(date__gte=now, date__lte=untilDate)
        occupied = []
        for reservation in reservations:
            if reservation.paid==True or reservation.reservation_date >= now - timedelta(days=1):
                occupied.append(reservation.date.strftime("%Y-%m-%d"))
        return occupied
