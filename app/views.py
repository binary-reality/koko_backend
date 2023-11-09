from django.shortcuts import render
from django.http import HttpResponse
from . import models
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from mine import final
import os
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
        return JsonResponse(json_obj, status = 200)
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
        return JsonResponse(json.loads(login_response.text), status = 200)
    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status = 405)
    
@csrf_exempt
def read(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        audio = json_param['file']
        with open("./mine/hi.m4a", "rb") as ft:
            audio = ft.read()
        wave = json_param['wave']
        openid = json_param['openid']
        acc_fileName = "./mine/" + openid + "_tmp"
        with open(acc_fileName + ".mp3", "wb") as f:
            f.write(audio)
        result = final.main(acc_fileName + ".mp3", wave)
        print(result)
        os.remove(acc_fileName + ".json")
        os.remove(acc_fileName + ".mp3")
        os.remove(acc_fileName + ".wav")

        return JsonResponse(
            {
                "code": 0,
                "info": "Success in word analyzing",
                "result": result
            },
            status = 200
        )

    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status = 405)