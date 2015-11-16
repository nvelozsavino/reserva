from django.db import models
from datetime import datetime, timedelta


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.EmailField()
    inscription_date = models.DateField(auto_now=False, auto_now_add=True)
    def __unicode__(self):
        return self.name + ' ' + self.last_name

    
# class Place(models.Model):
#     name = models.CharField(max_length=200)
#     def __unicode__(self):
#         return self.name
    

class Reservation(models.Model):
    user = models.ForeignKey(User)
    date = models.DateField(blank=True, null=True, unique=True)
    qty = models.IntegerField(default=8)
    # place = models.ForeignKey(Place)
    paid = models.BooleanField(default=False)
    reservation_date=models.DateTimeField(auto_now=True)
    payment_confirmation = models.CharField(null=True, blank=True,max_length=200)

    def __unicode__(self):
        return self.name + ' ' + self.last_name

    @staticmethod
    def get_ocuped_dates(month=datetime.now().month, year= datetime.now().year):
        reservations = Reservation.objects.filter(date__month=month,date__year=year)

        days=[]
        for reservation in reservations:
            if reservation.paid is True or reservation.reservation_date>=datetime.now()-timedelta(days=1):
                days.append(reservation.date.day);
        return days

