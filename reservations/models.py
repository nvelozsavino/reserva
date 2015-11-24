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
        return unicode(self.user)

    @staticmethod
    def get_ocuped_dates(month=datetime.now().month, year=datetime.now().year):
        reservations = Reservation.objects.filter(date__gte=datetime.now())
        occupied = []
        for reservation in reservations:
            if reservation.paid is True or reservation.reservation_date >= datetime.now() - timedelta(days=1):
                occupied.append(str(reservation.date))
        return occupied
