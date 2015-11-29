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
from django.core.mail import send_mail

# Create your views here.

@login_required
def index(request):
    reservations= Reservation.objects.filter(user=request.user)
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
        return render(request,'reservations/new.html', data)

@login_required
def payment(request,reservation_id):
    reservation= get_object_or_404(Reservation, pk=reservation_id)
    user= request.user
    if user != reservation.user:
        return HttpResponseForbidden()
    if reservation.paid:
        redirect_url = reverse('reservation_info',kwargs={'reservation_id':reservation.pk})
        return HttpResponseRedirect(redirect_url)       

    stripe_key="pk_test_LTzee3NEdHl6M7MCaCJWWoch"
    data={
        'reservation':reservation,
        'amount':int(reservation.value*100),
        'error_exist': False,
        'error_msg': '',
        'stripe_key': stripe_key,
    }

    if request.method == 'POST':
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
                send_mail('Payment Success', 'Payment success.', 'from@example.com',[user.email], fail_silently=False)
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

def payment_success(request, reservation_id):
    reservation= get_object_or_404(Reservation, pk=reservation_id)
    if request.user != reservation.user:
        return HttpResponseForbidden()

    payment_info = json.loads(reservation.payment_confirmation)
    print reservation.qty    
    data = {'reservation': reservation, 'card': payment_info['source']['brand'], 'last4':payment_info['source']['last4'] }
    return render(request,"reservations/payment_success.html",data)

def getreserveddates(request, reservation_id):

    occuped={"used":Reservation.get_ocuped_dates(int(reservation_id))}
    return JsonResponse(occuped)

@login_required
def edit(request, reservation_id):
    reservation=get_object_or_404(Reservation,pk=reservation_id)
    if request.user != reservation.user:
        return HttpResponseForbidden()
    if reservation.paid:
        return HttpResponseForbidden()

    if request.method=='POST':
        form = ReservationForm(request.POST, instance=reservation)        
        if form.is_valid():
            print "Form valid"
            form.save()
            redirect_url = reverse('reservation_info',kwargs={'reservation_id':reservation.id})
            return HttpResponseRedirect(redirect_url)
        else:

            data = {
                'optionalText':'Form Invalid',
                'user': request.user,
                'form': form,
                'reservation':reservation,
            }
            return render(request, "reservations/edit.html", data)
    else:
        form = ReservationForm(instance=reservation)
        data = {
            'optionalText':'No POST',
            'user': request.user,
            'form': form,
            'reservation':reservation,
        }
        return render(request,"reservations/edit.html",data)


@login_required
def delete(request, reservation_id):
    reservation=get_object_or_404(Reservation,pk=reservation_id)
    if request.user != reservation.user:
        return HttpResponseForbidden()
    if reservation.paid:
        return HttpResponseForbidden()
    reservation.delete()
    redirect_url = reverse('reservations_index')
    return HttpResponseRedirect(redirect_url)
