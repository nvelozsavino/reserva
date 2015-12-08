from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received
from base64 import b64decode
import re
from models import Reservation
def process_payment(sender, **kwargs):
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Undertake some action depending upon `ipn_obj`.
        custom_code=b64decode(ipn_obj.custom)
        m=re.search('reservation=(\d*)',custom_code)
        try:
            reservation_id= int(m.group(1))
            reservation=Reservation.objects().filter(pk=reservation_id)
            reservation.pay()
        except Reservation.DoesNotExist:
            print "not exist"


    else:
        print "fallo"

valid_ipn_received.connect(process_payment)