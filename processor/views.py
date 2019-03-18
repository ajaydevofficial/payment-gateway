from django.shortcuts import render,redirect
from Document.models import document

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
    ORDER_ID = 0


    if request.method=='POST':
        pass

    return render(request,"index.html",context)
