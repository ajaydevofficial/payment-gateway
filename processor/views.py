from django.shortcuts import render,redirect
from Document.models import document
from order_payload.models import order_id
from order_success.models import order_success
from order_failure.models import order_failure
from django.views.decorators.csrf import csrf_exempt
from .checksum import *
import requests
import base64
import json
import cgi
from os import environ

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
        'CALLBACK_URL' : 'http://127.0.0.1:8000/response/',#this for staging_purpose use your own response url

    }
    if request.method=='POST':
        data_dict['CHECKSUMHASH'] = generate_checksum(data_dict,MERCHANT_KEY)
        param_dict = data_dict
        paytmURL = "https://securegw-stage.paytm.in/theia/processTransaction"
        context['paytm_code_head']="<h1 hidden>Merchant Check Out Page</h1></br><form method='post' action='"+paytmURL+"'name='f1'>"
        context['paytm_code']=''
        for key in param_dict:
            context['paytm_code']+= "<input type='hidden' name='" + key.strip() + "'value=" + param_dict[key].strip()+">"
        context['paytm_code']+="<script type='text/javascript'>"
        context['paytm_code']+="document.f1.submit();"
        context['paytm_code']+='</script>'
        context['paytm_code']+='</form>'
        order_id.objects.update(order_id = int(order_id.objects.all().values('order_id')[0]['order_id'] + 1) )
        request.session['CHECKSUMHASH'] = data_dict['CHECKSUMHASH']

    return render(request,"index.html",context)

@csrf_exempt
def response_page(request):
    context={}
    print("Content-type: text/html\n")
    if request.method=='POST':
        print(request.POST)
    MERCHANT_KEY = 'jKc6NjVk0T1eZ0Bg'

    respons_dict = request.POST.copy()
    checksum = request.POST['CHECKSUMHASH']

    if 'GATEWAYNAME' in respons_dict:
    	if respons_dict['GATEWAYNAME'] == 'WALLET':
    		respons_dict['BANKNAME'] = 'null';

        #use a checksum verifying function if needed

    if respons_dict['RESPCODE'] == '01':
        context = {
            'ORDER_ID':request.POST['ORDERID'],
            'TXN_AMOUNT':request.POST['TXNAMOUNT']
        }
        order_success.objects.create(
            order_id = request.POST['ORDERID'] ,
            txn_id = request.POST['TXNID'] ,
            txn_amount = request.POST['TXNAMOUNT'] ,
            txn_date = request.POST['TXNDATE'] ,
            currency = request.POST['CURRENCY'] ,
            status = request.POST['STATUS'] ,
            resp_msg = request.POST['RESPMSG'] ,
            payment_mode = request.POST['PAYMENTMODE'] ,
            gateway_name = request.POST['GATEWAYNAME'] ,
            bank_txn_id = request.POST['BANKTXNID'] ,
            bank_name = request.POST['BANKNAME']
        )

        return render(request,"success.html",context)

    else:
        try:
            order_failure.objects.create(

                order_id = request.POST['ORDERID'] ,
                txn_id = request.POST['TXNID'] ,
                txn_amount = request.POST['TXNAMOUNT'] ,
                txn_date = request.POST['TXNDATE'] ,
                currency = request.POST['CURRENCY'] ,
                status = request.POST['STATUS'] ,
                resp_msg = request.POST['RESPMSG'] ,
                payment_mode = request.POST['PAYMENTMODE'] ,
                gateway_name = request.POST['GATEWAYNAME'] ,
                bank_txn_id = request.POST['BANKTXNID'] ,
                bank_name = request.POST['BANKNAME']
            )
        except:
                pass

        return render(request,"unsuccess.html",context)


    return render(request,"success.html",context)
