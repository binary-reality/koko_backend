from django.shortcuts import render
from django.http import HttpResponse
from . import models
# Create your views here.

def helloView(request):
    testUnit = models.testUnit.objects.get(pk=1)
    
    return render(request, "index.html", {"testUnit": testUnit})
