from django.contrib import admin

# Register your models here.
from .models import User, Reservation

class ReservationInLine(admin.TabularInline):
    model=Reservation
    extra=0

class UserAdmin(admin.ModelAdmin):
    fieldsets = [
        ('User Information', {'fields': ['user_name', 'user_last_name', 'user_email']}),
        
    ]
    inlines = [ReservationInLine]
        

admin.site.register(User,UserAdmin)
# admin.site.register(Place)
