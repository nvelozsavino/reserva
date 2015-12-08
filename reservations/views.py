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
from paypal.standard.forms import PayPalPaymentsForm
from base64 import b64encode
import settings
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def index(request):
    return render(request, 'reservations/index.html')

@login_required
def reservation_list(request):
    Reservation.cancel_pending_reservations(user=request.user)
    reservations= Reservation.objects.filter(user=request.user)
    data = {'reservations': reservations}
    return render(request, 'reservations/reservation_list.html', data)

@login_required
def edit(request, reservation_id=None):
    Reservation.cancel_pending_reservations(user=request.user)
    user = request.user
    if reservation_id != None:
        reservation=get_object_or_404(Reservation,pk=reservation_id)
        if reservation.user !=user or reservation.is_cancelled():
            return HttpResponseForbidden()
        edit=True
    else:
        reservation=Reservation()
        reservation.user=user
        edit=False
    form = ReservationForm(instance=reservation)
    data = {
        'user': user,
        'form': form,
        'edit': edit,
        'reservation': reservation,
    }
    if request.method == 'POST':
        form = ReservationForm(request.POST, instance=reservation)
        print ("Post")
        if form.is_valid():
            reservation=form.save(commit=False)
            reservation.save()
            #jump to payment processing
            redirect_url = reverse('reservation_payment',kwargs={'reservation_id':reservation.pk})
            return HttpResponseRedirect(redirect_url)
        else:
            data['form']=form
            return render(request, 'reservations/edit.html', data)
    #else:
    return render(request,'reservations/edit.html', data)

@login_required
def payment(request,reservation_id):
    reservation= get_object_or_404(Reservation, pk=reservation_id)
    user= request.user
    if user != reservation.user or reservation.is_cancelled():
        return HttpResponseForbidden()
    if reservation.is_paid():
        redirect_url = reverse('reservation_info',kwargs={'reservation_id':reservation.pk})
        return HttpResponseRedirect(redirect_url)       

    stripe_key="pk_test_LTzee3NEdHl6M7MCaCJWWoch"
    invoiceId= b64encode('invoice='+unicode(reservation.pk))
    customId= b64encode('reservation='+unicode(reservation.pk))
    paypal_dict = {
        "business": settings.PAYPAL_RECEIVER_EMAIL,
        "amount": reservation.value,
        "item_name": unicode(reservation),
        "invoice": invoiceId,
        "notify_url": settings.SITE_URL + reverse('paypal-ipn'),
        "return_url": settings.SITE_URL + reverse('paypal_return'),
        "cancel_return": settings.SITE_URL + reverse('reservation_payment', kwargs={'reservation_id':reservation_id}),#paypal_cancel_return'),
        "custom": customId,  # Custom command to correlate to some function later (optional)
    }

    # Create the instance.
    paypal_form = PayPalPaymentsForm(initial=paypal_dict)



    data={
        'reservation':reservation,
        'amount':int(reservation.value*100),
        'error_exist': False,
        'error_msg': '',
        'stripe_key': stripe_key,
        'paypal_form':paypal_form,
    }

    if request.method == 'POST': #Stripe processing only
        print "Method is POST"
        form = PaymentForm(request.POST)
        if form.is_valid():
            print "Form is valid"
            token = form.cleaned_data['stripeToken']           
            stripe.api_key = "sk_test_HthF4Hs8I4oGjA39RFdTDwko"
            try:
                charge = stripe.Charge.create(
                    amount=int(reservation.value*100),
                    currency="usd",
                    source=token,
                    description=unicode(reservation)
                )
                card_error=False
            except stripe.error.CardError,e:
                card_error=True
                card_error_msg=unicode(e)
                print "Error: exception " + unicode(e)
            if card_error is False:
                print "No Error" 
                reservation.pay(json.dumps(charge))
                redirect_url = reverse('payment_success',kwargs={'reservation_id':reservation.pk})
                return HttpResponseRedirect(redirect_url)                 
            else:
                print "Error"
                data['error_msg']=card_error_msg
                data['error_exist']=True
    else:
        print "Method is not POST"
    return render(request,'reservations/payment.html',data)

@login_required
def info(request,reservation_id):
    reservation= get_object_or_404(Reservation, pk=reservation_id)
    if request.user != reservation.user:
        return HttpResponseForbidden()
    return render(request,'reservations/info.html',{'reservation': reservation})

@login_required
def payment_success(request, reservation_id):
    reservation= get_object_or_404(Reservation, pk=reservation_id)
    if request.user != reservation.user:
        return HttpResponseForbidden()

    payment_info = json.loads(reservation.payment_confirmation)
    data = {'reservation': reservation, 'card': payment_info['source']['brand'], 'last4':payment_info['source']['last4'] }
    return render(request,"reservations/payment_success.html",data)

@login_required
def get_reserved_dates(request, reservation_id):
    occuped={"used":Reservation.get_ocuped_dates(int(reservation_id))}
    return JsonResponse(occuped)

def cancel_pending_reservations(request):
    cancelled = {"cancelled":Reservation.cancel_pending_reservations()}
    return JsonResponse(cancelled)

@login_required
def delete(request, reservation_id):
    reservation=get_object_or_404(Reservation,pk=reservation_id)
    if request.user != reservation.user:
        return HttpResponseForbidden()
    if reservation.paid:
        return HttpResponseForbidden()
    reservation.delete()
    redirect_url = reverse('reservations_list')
    return HttpResponseRedirect(redirect_url)

@csrf_exempt
def paypal_return(request):
    redirect_url = reverse('reservations_list')
    return HttpResponseRedirect(redirect_url)

def paypal_cancel_return(request):
    pass
