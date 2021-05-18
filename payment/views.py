from django import forms
from django.shortcuts import render, redirect

from django_coinpayments.models import Payment
from django_coinpayments.exceptions import CoinPaymentsProviderError
from django.views.generic import FormView, ListView, DetailView
from django.shortcuts import render, get_object_or_404
from decimal import Decimal
import requests
import json

from coinpayments import CoinPaymentsAPI

from json import dumps
import time


import ssl
ssl._create_default_https_context = ssl._create_unverified_context


class ExamplePaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ['amount']


'''def cheak(request,context,iid):
    print(iid.status_url)
    r = requests.get(url = iid.status_url)
    #json_data = json.loads(r.text)
    #print(json_data)
    return render(request, 'home_templates/payment_result.html', context)'''


def create_tx(request, payment):
    context = {}
    try:
        tx = payment.create_tx()
        print(tx, type(tx))

        api = CoinPaymentsAPI(public_key='4b4f7c51d0583384f082cc6894b40149063f17036da52bd7b7965a18fc53e89d',
                              private_key='b33162fc07f678eaB1d9aab22e5dc739eDb8a5030a0748e58bd7763F604cA4bd')

        payment.status = Payment.PAYMENT_STATUS_PENDING
        payment.save()
        print("hiiiii", payment)

        context['object'] = payment
        context['tx'] = tx

    except CoinPaymentsProviderError as e:
        context['error'] = e

    request.session['tx_id'] = payment.provider_tx.id
    request.session['address'] = payment.provider_tx.address
    request.session['qr_code'] = payment.provider_tx.qrcode_url
    return redirect('cheak')

    # render(request, 'home_templates/payment_result.html', context)
    return render(request, 'home_templates/payment_result.html', context)


class PaymentDetail(DetailView):
    model = Payment
    template_name = 'home_templates/payment_result.html'
    context_object_name = 'object'


class PaymentSetupView(FormView):
    template_name = 'home_templates/payment_setup.html'
    form_class = ExamplePaymentForm

    def form_valid(self, form):
        cl = form.cleaned_data
        payment = Payment(currency_original='TRX',
                          currency_paid='TRX',
                          amount=cl['amount'],
                          amount_paid=Decimal(0),
                          status=Payment.PAYMENT_STATUS_PROVIDER_PENDING,
                          )

        return create_tx(self.request, payment)


class PaymentList(ListView):
    model = Payment
    template_name = 'home_templates/payment_list.html'


def create_new_payment(request, pk):
    payment = get_object_or_404(Payment, pk=pk)
    if payment.status in [Payment.PAYMENT_STATUS_PROVIDER_PENDING, Payment.PAYMENT_STATUS_TIMEOUT]:
        pass
    elif payment.status in [Payment.PAYMENT_STATUS_PENDING]:
        payment.provider_tx.delete()
    else:
        error = "Invalid status - {}".format(payment.get_status_display())
        return render(request, 'home_templates/payment_result.html', {'error': error})
    return create_tx(request, payment)


def index(request):
    pub_key = '4b4f7c51d0583384f082cc6894b40149063f17036da52bd7b7965a18fc53e89d'
    pri_key = 'b33162fc07f678eaB1d9aab22e5dc739eDb8a5030a0748e58bd7763F604cA4bd'

    client = CryptoPayments(pub_key, pri_key,)

    return render(request, 'home_templates/index.html', d)


'''def cheak(request, txid):
    pub_key = '4b4f7c51d0583384f082cc6894b40149063f17036da52bd7b7965a18fc53e89d'
    pri_key = 'b33162fc07f678eaB1d9aab22e5dc739eDb8a5030a0748e58bd7763F604cA4bd'

    if not txid:
        return False
    params={}
    params.update({'cmd':'get_tx_info',
                       'key':pub_key,
                       'txid': txid,
                       })
    return render(request,'home_templates/info.html')'''


def ipn_view(request):
    p = request.POST
    ipn_mode = p.get('ipn_mode')
    if ipn_mode != 'hmac':
        return HttpResponseBadRequest('IPN Mode is not HMAC')
    http_hmac = request.META.get('HTTP_HMAC')
    if not http_hmac:
        return HttpResponseBadRequest('No HMAC signature sent.')
    our_hmac = create_ipn_hmac(request)
    print("Our hmac == server hmac - {res}" %
          {'res': str(our_hmac == http_hmac)})

    merchant_id = getattr(settings, 'COINPAYMENTS_MERCHANT_ID', None)
    if p.get('merchant') != merchant_id:
        return HttpResponseBadRequest('Invalid merchant id')
    tx_id = p.get('txn_id')
    payment = Payment.objects.filter(provider_tx_id__exact=tx_id).first()
    if payment:
        if payment.currency_original != p.get('currency1'):
            return HttpResponseBadRequest('Currency mismatch')
        if payment.status != Payment.PAYMENT_STATUS_PAID:
            # Payments statuses: https://www.coinpayments.net/merchant-tools-ipn
            # Safe statuses: 2 and >= 100
            status = int(p['status'])
            if status == 2 or status >= 100:
                logger.info('Received payment for transaction {} - payment {} ({})'
                            .format(str(tx_id), str(payment.id), str(payment.amount)))
                payment.amount_paid = payment.amount
            else:
                payment.amount_paid = Decimal(p['received_amount'])
            if payment.amount_paid == payment.amount:
                payment.status = Payment.PAYMENT_STATUS_PAID
            payment.save()
    return render(request, 'index.html')


def cheak(request):

    tx_id = request.session['tx_id']
    address = request.session['address']
    qr_code = request.session['qr_code']

    i = 0
    i = i+1

    api = CoinPaymentsAPI(public_key='4b4f7c51d0583384f082cc6894b40149063f17036da52bd7b7965a18fc53e89d',
                          private_key='b33162fc07f678eaB1d9aab22e5dc739eDb8a5030a0748e58bd7763F604cA4bd')

    k = api.get_tx_info(txid=tx_id)
    d1 = k['result']
    if d1['status'] == 1:
        return redirect('payment_list')
    d = {
        'data': k,
        'address': address,
        'i': i,
        'qr_code': qr_code,
    }
    return render(request, 'home_templates/cheak.html', d)


def success(request):
    return render(request, 'home_templates/success.html')