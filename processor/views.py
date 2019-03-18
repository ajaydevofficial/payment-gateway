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
    MID = 'KLUIOi74399454829212' #use your test or original MID from paytm buisness account
    ORDER_ID = str(order_id.objects.all().values('order_id')[0]['order_id'])
    CUST_ID = 'Customer_ID' #use different ID for different customers
    TXN_AMOUNT = 1.00 #change value accordingly
    CHANNEL_ID = 'WEB'
    WEBSITE = 'WEBSTAGING'
    INDUSTRY_TYPE_ID = 'Retail'
    CALLBACK_URL = 'http://127.0.0.1:8000/completed'


    if request.method=='POST':
        CHECKSUMHASH = ''


    return render(request,"index.html",context)
