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
            'date':forms.TextInput(attrs={'class':'datepicker'}),
        }

    def __init__(self, *args, **kwargs):
        super(ModelForm, self).__init__(*args, **kwargs)
        self.fields['qty'].max_value=12
        self.fields['qty'].min_value=1

        