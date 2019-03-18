from django.shortcuts import render,redirect
from Document.models import document

def home_page(request):
    context = {}
    try:
            doc = document.objects.get(name="Integration Docs")
            context = {'file':doc}

            return render(request,"index.html",context)
    except:
        print("File not in Database")
    return render(request,"index.html",context)
