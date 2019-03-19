from django.shortcuts import render,redirect
from Document.models import document
from order_payload.models import order_id
from .checksum import *
import requests
import base64
import json

def home_page(request):
    context = {}
    #code for downloading Integration Docs File from Template
    try:
            doc = document.objects.get(name="Integration Docs")
            context = {'file':doc}
    except:
        pass
    #order-paylod variables which are mandatory
    MERCHANT_KEY = 'jKc6NjVk0T1eZ0Bg'
    data_dict = {

        'MID' :'KLUIOi74399454829212', #use your test or original MID from paytm buisness account
        'ORDER_ID' : str(order_id.objects.all().values('order_id')[0]['order_id']),
        'CUST_ID' : 'Customer_ID', #use different ID for different customers
        'TXN_AMOUNT' : '1.00', #change value accordingly
        'CHANNEL_ID' : 'WEB',
        'WEBSITE' : 'WEBSTAGING',
        'INDUSTRY_TYPE_ID' : 'Retail',
        'CALLBACK_URL' : 'http://127.0.0.1:1234/success',

    }

    if request.method=='POST':
        data_dict['CHECKSUMHASH'] = generate_checksum(data_dict,MERCHANT_KEY)
        param_dict = data_dict
        paytmURL = "https://securegw-stage.paytm.in/theia/processTransaction"
        context['paytm_code']="<h1 hidden>Merchant Check Out Page</h1></br><form method='post' action='"+paytmURL+"'name='f1'>"
        for key in param_dict:
            context['paytm_code']+="<input type='hidden' name='" + key.strip() + "'value=" + param_dict[key].strip()+">"
        context['paytm_code']+="<script type='text/javascript'>"
        context['paytm_code']+="document.f1.submit();"
        context['paytm_code']+='</script>'
        context['paytm_code']+='</form>'


    return render(request,"index.html",context)
