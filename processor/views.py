from django.shortcuts import render,redirect
from Document.models import document
from order_payload.models import order_id
from order_success.models import order_success
from order_failure.models import order_failure
from order_refund.models import order_refund
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

        'MID'              :'KLUIOi74399454829212', #use your test or original MID from paytm buisness account
        'ORDER_ID'         : str(order_id.objects.get(name='ORDER_ID').id),
        'CUST_ID'          : 'Customer_ID', #use different ID for different customers
        'TXN_AMOUNT'       : '1.00', #change value accordingly
        'CHANNEL_ID'       : 'WEB',
        'WEBSITE'          : 'WEBSTAGING',
        'INDUSTRY_TYPE_ID' : 'Retail',
        'CALLBACK_URL'     : 'http://127.0.0.1:8000/response/',#this for staging_purpose use your own response url

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
        request.session['CHECKSUMHASH'] = data_dict['CHECKSUMHASH']

    return render(request,"index.html",context)


@csrf_exempt
def response_page(request):

    context={}
    MERCHANT_KEY = 'jKc6NjVk0T1eZ0Bg'
    print(order_id.objects.get(name="REF_ID").id)

    data_dict = {

        'MID'      :'KLUIOi74399454829212', #use your test or original MID from paytm buisness account
        'ORDER_ID' : str(order_id.objects.get(name='ORDER_ID').id),
    }

    data_dict['CHECKSUMHASH'] = generate_checksum(data_dict,MERCHANT_KEY)
    order_id.objects.update(order_id = int(order_id.objects.get(name="ORDER_ID").id) + 1)
    response = requests.get('https://securegw-stage.paytm.in/merchant-status/getTxnStatus?'+'JsonData='+str(data_dict))


    respons_dict = response.json()


    if 'GATEWAYNAME' in respons_dict:
    	if respons_dict['GATEWAYNAME'] == 'WALLET':
    		respons_dict['BANKNAME'] = 'null';

        #use a checksum verifying function if needed

    if respons_dict['RESPCODE'] == '01':
        context = {
            'ORDER_ID':respons_dict['ORDERID'],
            'TXN_AMOUNT':respons_dict['TXNAMOUNT']
        }
        order_success.objects.create(
            order_id = respons_dict['ORDERID'] ,
            txn_id = respons_dict['TXNID'] ,
            txn_amount = respons_dict['TXNAMOUNT'] ,
            txn_date = respons_dict['TXNDATE'] ,
            currency = request.POST['CURRENCY'] ,
            status = respons_dict['STATUS'] ,
            resp_msg = respons_dict['RESPMSG'] ,
            payment_mode = respons_dict['PAYMENTMODE'] ,
            gateway_name = respons_dict['GATEWAYNAME'] ,
            bank_txn_id = respons_dict['BANKTXNID'] ,
            bank_name = respons_dict['BANKNAME']
        )
        if respons_dict['REFUNDAMT']!='0.00':
            order_refund.objects.create(
                order_id = respons_dict['ORDERID'] ,
                txn_id = respons_dict['TXNID'] ,
                txn_amount = respons_dict['TXNAMOUNT'] ,
                txn_date = respons_dict['TXNDATE'] ,
                currency = request.POST['CURRENCY'] ,
                status = respons_dict['STATUS'] ,
                resp_msg = respons_dict['RESPMSG'] ,
                payment_mode = respons_dict['PAYMENTMODE'] ,
                gateway_name = respons_dict['GATEWAYNAME'] ,
                bank_txn_id = respons_dict['BANKTXNID'] ,
                bank_name = respons_dict['BANKNAME'],
                refund_amount = respons_dict['REFUNDAMT']
            )
            refund_dict = {

                'MID'         : 'KLUIOi74399454829212',
                'REFID'       : str(order_id.objects.get(name='REF_ID')),
                'TXNID'       : respons_dict['TXNID'],
                'ORDERID'     : respons_dict['ORDERID'],
                'REFUNDAMOUNT': respons_dict['REFUNDAMT'],
                'TXNTYPE'     : 'REFUND',

            }
            refund_dict['CHECKSUM'] = generate_refund_checksum(refund_dict, MERCHANT_KEY, salt=None)
            refund_response = requests.get(
                "https://securegw-stage.paytm.in/refund/HANDLER_INTERNAL/REFUND?" +
                "JsonData="+
                str(refund_dict)
            )
            refund_response_dict = refund_response.json()
            print(refund_response_dict)

        return render(request,"success.html",context)

    else:
        if respons_dict['REFUNDAMT']!='0.00':
            order_refund.objects.create(
                order_id = respons_dict['ORDERID'] ,
                txn_id = respons_dict['TXNID'] ,
                txn_amount = respons_dict['TXNAMOUNT'] ,
                txn_date = respons_dict['TXNDATE'] ,
                currency = request.POST['CURRENCY'] ,
                status = respons_dict['STATUS'] ,
                resp_msg = respons_dict['RESPMSG'] ,
                payment_mode = respons_dict['PAYMENTMODE'] ,
                gateway_name = respons_dict['GATEWAYNAME'] ,
                bank_txn_id = respons_dict['BANKTXNID'] ,
                bank_name = respons_dict['BANKNAME'],
                refund_amount =respons_dict['REFUNDAMT']
            )
            refund_dict = {

                'MID'         : 'KLUIOi74399454829212',
                'REFID'       : str(order_id.objects.get(name='REF_ID')),
                'TXNID'       : respons_dict['TXNID'],
                'ORDERID'     : respons_dict['ORDERID'],
                'REFUNDAMOUNT': respons_dict['REFUNDAMT'],
                'TXNTYPE'     : 'REFUND',

            }
            refund_dict['CHECKSUM'] = generate_refund_checksum(refund_dict, MERCHANT_KEY, salt=None)
            refund_response = requests.get(
                "https://securegw-stage.paytm.in/refund/HANDLER_INTERNAL/REFUND?" +
                "JsonData="+
                str(refund_dict)
            )
            refund_response_dict = refund_response.json()
            print(refund_response_dict)

        try:
            order_failure.objects.create(

                order_id = respons_dict['ORDERID'] ,
                txn_id = respons_dict['TXNID'] ,
                txn_amount = respons_dict['TXNAMOUNT'] ,
                txn_date = respons_dict['TXNDATE'] ,
                currency = request.POST['CURRENCY'] ,
                status = respons_dict['STATUS'] ,
                resp_msg = respons_dict['RESPMSG'] ,
                payment_mode = respons_dict['PAYMENTMODE'] ,
                gateway_name = respons_dict['GATEWAYNAME'] ,
                bank_txn_id = respons_dict['BANKTXNID'] ,
                bank_name = respons_dict['BANKNAME']
            )
        except:
                pass

        return render(request,"unsuccess.html",context)


    return render(request,"success.html",context)
