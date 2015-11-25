from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from models import Reservation
from django.template import RequestContext
from forms import ReservationForm
from django.core.urlresolvers import reverse
# from users.models import WebUser,Address,Email,Phone
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404, HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
import json
from datetime import datetime, timedelta

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
    data={
        'reservation':reservation
    }
    return render_to_response('reservations/payment.html',data, context_instance=RequestContext(request))

def getreserveddates(request,month,year):
    reservations = Reservation.objects.filter(date__gte=datetime.now())
    oc=[]
    for reservation in reservations:
        resmonth=reservation.date.strftime("%m")
        resyear = reservation.date.strftime("%Y")
        if resmonth==month and resyear==year and reservation.paid==False:
            oc.append(reservation.date.strftime("%Y-%m-%d"))
    #return HttpResponse(oc)
    return JsonResponse(json.dumps(oc),safe=False)#Reservation.get_ocuped_dates(month,year)),safe=False)
