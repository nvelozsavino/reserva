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
    def get_ocuped_dates(month, year):
        reservations = Reservation.objects.filter(date__gte=datetime.now())
        occupied = []
        for reservation in reservations:

            if reservation.paid==False and reservation.date.strftime("%m")==month and reservation.date.strftime("%Y")==year:
                occupied.append(reservation.date.strftime("%Y-%m-%d"))
        return occupied
