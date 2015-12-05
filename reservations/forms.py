from django import forms
from django.forms import ModelForm, DateInput
from models import Reservation, User
from registration.forms import RegistrationForm


class UserForm(RegistrationForm):
    class Meta:
        model=RegistrationForm.Meta.model
        fields=RegistrationForm.Meta.fields+('first_name','last_name',)

class ReservationForm(ModelForm):
    class Meta:
        model = Reservation
        fields = ['qty', 'date']
        widgets = {
            'date':forms.DateInput(attrs={'class':'datepicker'}, format="%m/%d/%Y"),
        }



class PaymentForm(forms.Form):
    stripeToken = forms.CharField()
    stripeTokenType = forms.CharField()
    stripeEmail = forms.EmailField()


       
        
