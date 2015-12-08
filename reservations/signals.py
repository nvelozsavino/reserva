from paypal.standard.models import ST_PP_COMPLETED
from paypal.standard.ipn.signals import valid_ipn_received, invalid_ipn_received
from base64 import b64decode
import re
from models import Reservation
def process_payment(sender, **kwargs):
    print "Processing payment"
    ipn_obj = sender
    if ipn_obj.payment_status == ST_PP_COMPLETED:
        # Undertake some action depending upon `ipn_obj`.
        custom_code=b64decode(ipn_obj.custom)
        print "Custom Code: " + ipn_obj.custom + " decoded: " + custom_code
        m=re.search('reservation=(.*),(\d*)',custom_code)
        try:
            reservation_id= int(m.group(2))
            reservation=Reservation.objects().filter(pk=reservation_id)
            reservation.pay()
        except Reservation.DoesNotExist:
            print "not exist"


    else:
        print "fallo"


valid_ipn_received.connect(process_payment)
invalid_ipn_received.connect(process_payment)