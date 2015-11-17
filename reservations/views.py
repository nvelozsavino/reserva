from django.contrib.auth.decorators import login_required
from django.shortcuts import render, render_to_response
from models import Reservation
from django.template import RequestContext
from forms import ReservationForm
from django.core.urlresolvers import reverse
# from users.models import WebUser,Address,Email,Phone
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404, HttpResponse
from django.shortcuts import get_object_or_404

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