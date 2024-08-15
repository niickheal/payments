from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import urllib.parse

def get_upi_id():
    usage = 10
    upi_obj = UpiId.objects.filter(active=True).order_by('usage_count').first()
    upi_obj.usage_count += 1
    if upi_obj.usage_count > usage:
        upi_obj.active = False
    upi_obj.save()
    if upi_obj.upi_id:
        return upi_obj.upi_id
    else:
        return ''

def home(request):
    '''
    Fields	Description
    pa	Payee address or business virtual payment address (VPA).
    pn	Payee name or business name.
    mc	Business retailer category code.
    tr	Transaction reference ID. (Business specific ID. Must be unique for each request.)
    url	Transaction reference URL.
    am	Transaction amount. (Up to two decimal digits are allowed. This should be set in the details object instead of the supportedInstruments object.)
    cu	Currency code. (This should be set in the details object instead of supportedInstruments object. Only the Indian rupee (INR) is currently supported.)
    tid	Transaction ID generated by the payment service provider (PSP) of the business.
    tn	Transaction note. It is the description appearing in the Google Pay payflow. (Maximum length is 80 characters)
    gstBrkUp	Break-up of Goods and Services Tax. This should follow the format: `GST:amount
    invoiceNo	Invoice Number. Identifier of a bill/invoice.
    invoiceDate	The time of invoice in RFC 3339 format. Eg, 2017-02-15T16:20:30+05:30 for IST timezone).
    gstIn	Business GSTIN. Goods and Services Tax Identification Number.

    upi://pay?tr=202101345671229366&tid=121313202101345671229366&pa=juspay@axisbank&mc=1234&pn= Merchant%20Inc&am=1.00&cu=INR&tn=Pay%20for%20merchant
    upi://pay?tr=...(enter the tr).......&tid=...(enter the tid).......&pa=.....(enter merchant_vpa)...&mc=....(enter the mcc)...&pn=....(enter
the Merchant name)...&am=.....(enter the amount).....&cu=INR&tn=....(description for the transaction)..
    '''
    context = {
        'upi_table' : UpiId.objects.all()
    }
    if request.method == "POST":
        upi_id = get_upi_id()
        if upi_id:
            if request.POST.get('upi_app') == 'gpay':
                upi_app = 'tez://upi/pay'
            elif request.POST.get('upi_app') == 'phonepe':
                upi_app = 'phonepe://pay'
            elif request.POST.get('upi_app') == 'paytm':
                upi_app = 'paytmmp://pay'
            else:
                upi_app = 'upi://pay'
            redirect_url = upi_app + "?pa=" + urllib.parse.quote_plus(upi_id) + "&am=" + request.POST['amount'] + "&tn=" + urllib.parse.quote_plus(request.POST['desc']) + "&pn="+ urllib.parse.quote_plus("Nikhil Mhatre")
            context['upi'] = redirect_url
        else:
            context['upi'] = 'UPI ID NOT available'
    return render(request,'index.html',context)

def bankpayout(request):
    if request.method == "POST":
        try:
            BankPayout.objects.create(
                **json.loads(request.body)
            )
            return JsonResponse({'status':'successfull'})
        except:
            return JsonResponse({'status':'failed'})
