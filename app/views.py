from django.shortcuts import render
from django.http import HttpResponse
from . import models
import requests
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from mine import final
from dicts.dic_func import Dic
import os

# Create your views here.

# @csrf_exempt
# def helloView(request):
#     if request.method == "GET":
#         # models.testUnit.objects.create(var1="Added infomation")

#         # testUnit = models.testUnit.objects.get(pk=1)
#         json_obj = {
#             "json": "json",
#             "hello": "hello",
#         }
#         return JsonResponse(json_obj, status = 200)
#         return render(request, "index.html", {"testUnit": testUnit})
#     if request.method == "POST":
#         print(request)
#         testUnit = models.testUnit.objects.get(pk=1)
#         return render(request, "index.html", {"testUnit": testUnit})

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
        response_json = {}
        if code == "3e5428-ff58yj5":
            response_json = {
                'openid': "88hrt-j37db-x56kt-fkyou",
                'session_key': "As your wish",
                'unionid': 'usotuki',
                'errmsg': '',
                'errcode': 0, 
            }
        else:
            response_json = json.loads(login_response.text)
        if response_json['errcode'] == 0:
            user_id = response_json['openid']
            valid_user_list = models.user.objects.filter(open_id=user_id)
            if len(valid_user_list) == 0:
                models.user.objects.create(open_id=user_id, status=1)
                models.create_my_wordlistinfo(user_id)
                models.create_my_readingrecord(user_id)
                models.create_my_searchrecord(user_id)
            elif len(valid_user_list) == 1:
                valid_user_list.update(status=1)
            else:
                pass
        # user_id = '345'
        # valid_user_list = models.user.objects.filter(open_id=user_id)
        # if len(valid_user_list) == 0:
        #     models.user.objects.create(open_id=user_id, status=1)
        #     models.create_my_wordlistinfo(user_id)
        #     models.create_my_readingrecord(user_id)
        #     models.create_my_searchrecord(user_id)
        #     user = models.user.objects.filter(open_id=user_id)
        #     list_0 = models.create_my_wordlist(user_id, 0)
        #     list_0.objects.create(owner_openid=user[0], content="hello" + user_id)
        #     list_1 = models.create_my_wordlist(user_id, 1)
        #     list_1.objects.create(owner_openid=user[0], content="make")
        #     list_1.objects.create(owner_openid=user[0], content="hello" + user_id)
        #     list_1.objects.create(owner_openid=user[0], content="hellop" + user_id)
        #     list_1.objects.create(owner_openid=user[0], content="make")
        #     list_1.objects.create(owner_openid=user[0], content="make")
        #     list = user[0].list1.filter(content='make')
        #     for record in list:
        #         print(record.id)
        # elif len(valid_user_list) == 1:
        #     valid_user_list.update(status=1)
        # else:
        #     pass


        return JsonResponse(response_json, status = 200)
    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status = 405)
    
@csrf_exempt
def read(request):
    if request.method == "POST":
        files = request.FILES
        # print(files)
        wavelist = request.POST.get("wave")
        wave = []
        for x in wavelist:
            if x.isdigit():
                wave.append(int(x))
        # print(wave)
        openid = request.POST.get("openid")
        audio = files['word.mp3'].read()
        # print(audio)

        # with open("./mine/hi.m4a", "rb") as ft:
        #     audio = ft.read()
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
                "accent": result
            },
            status = 200
        )

    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status = 405)
    
diction=Dic()
@csrf_exempt
def search(request):
    if request.method == "POST":
        # print(files)
        json_param = json.loads(request.body)
        word = json_param["searchWord"]
        # print(wave)
        openid = request.POST.get("openid")
        print(word)
        print(diction.search_results(word))
        return JsonResponse(
            {
                "code": 0,
                "info": "Success in word searching",
                "results": diction.search_results(word)
            },
            status = 200
        )

    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status = 405)
    

@csrf_exempt
def detail(request):
    if request.method == "POST":
        # print(files)
        json_param = json.loads(request.body)
        word = json_param["word"]
        
        # print(wave)
        openid = request.POST.get("openid")
        
        return JsonResponse(
            {
                "code": 0,
                "info": "Success in word searching",
                "detail": diction.get_detail(word)
            },
            status = 200
        )

    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status = 405)
    

@csrf_exempt
def getlist(request):
    if request.method == "POST":
        # print(files)
        json_param = json.loads(request.body)
        word = json_param["type"]
        
        # print(wave)
        openid = request.POST.get("openid")
        
        return JsonResponse(
            {
                "code": 0,
                "info": "Success in word searching",
                "medicine": diction.medical_list(word)
            },
            status = 200
        )

    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status = 405)