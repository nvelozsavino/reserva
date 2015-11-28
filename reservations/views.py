from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from models import Reservation
from django.template import RequestContext
from forms import ReservationForm, PaymentForm
from django.core.urlresolvers import reverse
# from users.models import WebUser,Address,Email,Phone
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
import json
from datetime import datetime, timedelta
import stripe

# Create your views here.

def index(request):
    reservations= Reservation.objects.all()

    data = {'reservations': reservations}
    return render_to_response('reservations/index.html', data, context_instance=RequestContext(request))

@login_required
def new(request):
    user = request.user
    if request.method == 'POST':
        print ("Post")
        form = ReservationForm(request.POST)
        if form.is_valid():
            reservation=form.save(commit=False)
            reservation.user=user
            reservation.save()
            #jump to payment processing
            redirect_url = reverse('reservation_payment',kwargs={'reservation_id':reservation.id})
            return HttpResponseRedirect(redirect_url)
        else:
            data = {
                'user': user,
                'form': form,
            }
            return render(request, 'reservations/new.html', data)

    else:
        reservation=Reservation()
        reservation.user=user
        form = ReservationForm(instance=reservation)
        data = {
            'user': user,
            'form': form,
        }
        return render_to_response('reservations/new.html', data, context_instance=RequestContext(request))

@login_required
def payment(request,reservation_id):
    reservation= get_object_or_404(Reservation, pk=reservation_id)
    if reservation.paid:
        redirect_url = reverse('reservation_info',kwargs={'reservation_id':reservation.pk})
        return HttpResponseRedirect(redirect_url)       

    stripe_key="pk_test_LTzee3NEdHl6M7MCaCJWWoch"
    data={
        'reservation':reservation,
        'error_exist': False,
        'error_msg': '',
        'stripe_key': stripe_key,
    }

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            token = form.cleaned_data['stripeToken']           
            stripe.api_key = "sk_test_HthF4Hs8I4oGjA39RFdTDwko"
            try:
                charge = stripe.Charge.create(
                    ammount=reservation.value,
                    currency="usd",
                    source=token,
                    description=unicode(reservation)
                )
                card_error=False
            except stripe.error.CardError,e:
                card_error=True
                card_error_msg=unicode(e)
            if card_error is False:
                reservation.pay(charge)
                redirect_url = reverse('payment_success',kwargs={'reservation_id':reservation.pk})
                return HttpResponseRedirect(redirect_url)                 
            else:
                data['error_msg']=card_error_msg
                data['error_exist']=True
                return HttpResponse("Error")
    return render(request,'reservations/payment.html',data)

@login_required
def info(request,reservation_id):
    reservation= get_object_or_404(Reservation, pk=reservation_id)
    return render(request,'reservations/info.html',{'reservation_id': reservation.pk})

def payment_success(request, reservation_id):
    reservation= get_object_or_404(Reservation, pk=reservation_id)
    data = {'reservation': reservation }
    return render(request,"reservations/payment_success.html",data)

def getreserveddates(request):
    occuped={"used":Reservation.get_ocuped_dates()}
    return JsonResponse(occuped)
