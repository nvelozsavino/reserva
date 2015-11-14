from django.db import models

# Create your models here.
class User(models.Model):
    user_name = models.CharField(max_length=200)
    user_last_name = models.CharField(max_length=200)
    user_email = models.EmailField(max_length=254)
    user_inscription_date = models.DateField(auto_now=False, auto_now_add=True)
    def __unicode__(self):
        return self.user_name + ' ' + self.user_last_name

    
class Place(models.Model):
    name = models.CharField(max_length=200)
    def __unicode__(self):
        return self.name
    

class Reservation(models.Model):
    user = models.ForeignKey(User)
    reservation_date = models.DateTimeField()
    reservation_place = models.ForeignKey(Place)
    reservation_paid = models.BooleanField(default=False)
    reservation_payment_confirmation = models.CharField(max_length=200)
    
