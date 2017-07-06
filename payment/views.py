from django.shortcuts import render
from django.core.urlresolvers import reverse
from django.shortcuts import render,redirect
from paypal.standard.forms import PayPalPaymentsForm
from decimal import Decimal
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect

# Create your views here.




def payment_process(request):
    order_id = request.session('order_id')
    u = user_db.product_details.find_one({'shop_id': order_id})
    host = request.get_host()

    paypal_dict = {
        'business': "princesharzeel.10@gmail.com",
        'amount': '%.2f' % u.get_total_cost().quantize(Decimal('.01')),
        'item_name': u['ptitle'],
        'invoice': str(u['_id']),
        'notify_url': 'https://{}{}'.format(host, reverse('paypal-ipn'
                )),
        'return_url': 'https://{}{}'.format(host, reverse('paypal:done'
                )),
        'cancel_return': 'https://{}{}'.format(host,
                reverse('paypal:canceled')),
        }


    form = PayPalPaymentsForm(initial=paypal_dict)
    return render(request, 'payment/process.html', {'form': form,
              'order': order})


			


@csrf_exempt
def payment_done(request):
	return render(request,'payment/done.html')

@csrf_exempt
def payment_canceled(request):
	return render(request,'payment/cancel.html')