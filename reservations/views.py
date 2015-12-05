from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, authenticate, login
from django.shortcuts import render, render_to_response
from models import Reservation
from django.template import RequestContext
from forms import ReservationForm, PaymentForm
from django.core.urlresolvers import reverse
# from users.models import WebUser,Address,Email,Phone
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404, HttpResponse, JsonResponse

from django.shortcuts import get_object_or_404, redirect
import json
import settings
from datetime import datetime, timedelta
import stripe


# Create your views here.
def login_user(request):
    #logout(request)
    username = password = ''
    if request.POST:
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                #return HttpResponseRedirect(reverse('reservations_list'))
    return HttpResponseForbidden


def index(request):
    login_user(request)
    redirect_to = request.REQUEST.get('next', '')
    data={}
    data['logged']= request.user.is_authenticated()
    if request.user.is_authenticated():
        if redirect_to !="":
            return HttpResponseRedirect(redirect_to)
        else:
       # return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
            return HttpResponseRedirect(reverse('reservations_list'))

    return render(request, 'reservations/index.html', data)

def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse('reservations_index'))



@login_required(login_url='reservations_index')
def reservation_list(request):
    data={}
    data['logged']= request.user.is_authenticated()
    reservations= Reservation.objects.filter(user=request.user)
    data ['reservations']= reservations
    return render(request, 'reservations/reservation_list.html', data)

@login_required(login_url='reservations_index')
def edit(request, reservation_id=None):
    user = request.user
    if reservation_id != None:
        reservation=get_object_or_404(Reservation,pk=reservation_id)
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
    data['logged']= request.user.is_authenticated()
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
    if user != reservation.user:
        return HttpResponseForbidden()
    if reservation.status=='P':
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
    data['logged']= request.user.is_authenticated()
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
    data={}
    data['logged']= request.user.is_authenticated()


    reservation= get_object_or_404(Reservation, pk=reservation_id)
    if request.user != reservation.user:
        return HttpResponseForbidden()
    data['reservation']=reservation
    return render(request,'reservations/info.html',data)

def payment_success(request, reservation_id):
    reservation= get_object_or_404(Reservation, pk=reservation_id)
    if request.user != reservation.user:
        return HttpResponseForbidden()

    payment_info = json.loads(reservation.payment_confirmation)
    print reservation.qty    
    data = {'reservation': reservation, 'card': payment_info['source']['brand'], 'last4':payment_info['source']['last4'] }
    data['logged']= request.user.is_authenticated()
    return render(request,"reservations/payment_success.html",data)

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
    redirect_url = reverse('reservations_index')
    return HttpResponseRedirect(redirect_url)
