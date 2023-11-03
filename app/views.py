from django.shortcuts import render
from django.http import HttpResponse
from . import models
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
# Create your views here.

@csrf_exempt
def helloView(request):
    if request.method == "GET":
        models.testUnit.objects.create(var1="Added infomation")

        testUnit = models.testUnit.objects.get(pk=1)
        json_obj = {
            "json": "json",
            "hello": "hello",
        }
        return JsonResponse(json_obj)
        return render(request, "index.html", {"testUnit": testUnit})
    if request.method == "POST":
        print(request)
        testUnit = models.testUnit.objects.get(pk=1)
        return render(request, "index.html", {"testUnit": testUnit})

@csrf_exempt
def login(request):

    if request.method == "POST":
        json_param = json.loads(request.body)
        code = json_param['code']
        # print(request)

        login_response = requests.get(
            url = "https://api.weixin.qq.com/sns/jscode2session",
            params = {
                "appid": "wx5ef6067498a5d631",
                "secret": "f72baea608e953e3d5850999d9667309",
                "js_code": code,
                "grant_type": "authorization_code"
            }
        )
        print(login_response.text)
        return JsonResponse(json.loads(login_response.text))
    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"})