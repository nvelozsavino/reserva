from django.contrib import admin

# Register your models here.
from models import Reservation

class ReservationInLine(admin.TabularInline):
    model=Reservation
    extra=0


# admin.site.register(Place)
