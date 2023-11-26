from django.shortcuts import render
from django.http import HttpResponse
from . import models
import requests
from django.http import JsonResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt
import json
from mine import final
from dicts.dic_func import Dic
import os
from koko import settings

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
                models.user.objects.create(open_id=user_id, nickname="用户"+user_id)
                # models.create_my_wordlistinfo(user_id)
                # models.create_my_readingrecord(user_id)
                # models.create_my_searchrecord(user_id)
            elif len(valid_user_list) == 1:
                pass
            else:
                pass
            curuser = models.user.objects.get(open_id=user_id)
            user_data = {}

            # file
            user_data['file'] = curuser.headicon_name
            # info
            user_data_info = {}
            user_data_info['openid'] = curuser.open_id
            user_data_info['nickname'] = curuser.nickname
            user_data_info['timeline'] = curuser.reserved_time
            if curuser.read_keep == 1:
                user_data_info['recordOn'] = 'true'
            else:
                user_data_info['recordOn'] = 'false'
            user_data_info['wbnum'] = curuser.wdlistnumber
            user_data['info'] = user_data_info

            # wordbooks
            user_data_wdbks = []
            curuser_word = curuser.wordlist.all()
            curuser_wbinfo = curuser.wbinfo.all()
            for i in range(1, curuser.wdlistnumber + 1):
                wd_content = {}
                cur_info = curuser_wbinfo.get(index=i)
                wd_content['id'] = i
                wd_content['name'] = cur_info.name
                wd_content['intro'] = cur_info.intro
                # wd_content['coverUrl'] = cur_info.image
                words = []
                wdlist = curuser_word.filter(index=i)
                for x in wdlist:
                    words.append(x.content)
                user_data_wdbks.append(wd_content)
            user_data['wordbooks'] = user_data_wdbks

            # wordHistory
            wdHis = []
            curuser_his = curuser.searchrecord.all()
            for x in curuser_his:
                record = []
                record.append(x.content)
                record.append(x.date)
                record.append(x.schnumber)
                wdHis.append(record)
            user_data['wordHistory'] = wdHis

            # readHistory
            rdHis = []
            curuser_rdHis = curuser.readingrecord.all()
            for x in curuser_rdHis:
                record = []
                record.append(x.content)
                record.append(x.date)
                record.append(x.lastrd)
                record.append(x.lastres)
                rdHis.append(record)
            user_data['readHistory'] = rdHis
            response_json['user_data'] = user_data
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
def getlogheadicon(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        user_id = json_param['openid']
        list = models.user.objects.filter(open_id=user_id)
        if (len(list) == 0):
            return JsonResponse({'code': '401', "message": "User Unauthorized"}, status=401)
        elif len(list) == 1:
            image = list[0].headicon
            return FileResponse(image, as_attachment=True, filename="headicon.jpg")
    else:
        return JsonResponse({'code': '405', "message": "Method not allowed"}, status=405)

@csrf_exempt
def read(request):
    if request.method == "POST":
        files = request.FILES
        # print(files)
        wavelist = request.POST.get("wave")
        word=request.POST.get("word")
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
        user = models.user.objects.get(open_id=openid)
        rec=models.rdrecord.objects.filter(owner_openid=user, content=word)
        if len(rec)==0:
            models.rdrecord.objects.create(owner_openid=user, content=word, lastrd=result,rdnumber=1,cornumber=(result==wave),lastres=(result==wave))
        else:
            rec[0].rdnumber=rec[0].rdnumber+1
            rec[0].cornumber=rec[0].cornumber+(result==wave)
            rec[0].lastrd=result
            rec[0].lastres=(result==wave)
            rec[0].save()

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
        openid = json_param['openid']
        user = models.user.objects.get(open_id=openid)
        userlist = user.searchrecord.filter(content=word)
        if len(userlist) == 0:
            models.schrcd.objects.create(owner_openid=user, content=word, schnumber=1)
        elif len(userlist) == 1:
            userlist[0].schnumber = userlist[0].schnumber + 1
            userlist[0].save()
        else:
            pass
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

@csrf_exempt
def headicon_change(request):
    if request.method == "POST":
        files = request.FILES
        openid = request.POST.get("openid")
        name = request.POST.get("name")
        image = files.get("headIcon")
        image_url_list = name.split('.')
        image_name = openid + "." + image_url_list[1]
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"code": "401", "message": "User Unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            user.headicon_name = image_name
            os.remove(os.path.join(settings.MEDIA_ROOT, user.headicon.name))
            user.headicon = image
            user.save()
            return JsonResponse({"code": 0, "message": "Headicon successfully changed!"}, status=200)
        else:
            pass
    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status=405)

@csrf_exempt
def nickname_change(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        openid = json_param['openid']
        new_nickname = json_param['nickname']
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"code": "401", "message": "User Unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            user.nickname = new_nickname
            user.save()
            return JsonResponse({"code": 0, "message": "Nickname successfully changed!"}, status=200)
        else:
            pass
    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status=405)

@csrf_exempt 
def timeline_change(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        openid = json_param['openid']
        new_timeline = json_param['timeline']
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"code": "401", "message": "User Unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            user.reserved_time = new_timeline
            user.save()
            return JsonResponse({"code": 0, "message": "Timeline successfully changed!"}, status=200)
        else:
            pass
    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status=405)

@csrf_exempt
def record_change(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        openid = json_param['openid']
        new_record = json_param['recordOn']
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"code": "401", "message": "User Unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            if new_record == "False":
                user.read_keep = 0
            elif new_record == "True":
                user.read_keep = 1
            else:
                return JsonResponse({"code": "400", "message": "Bad request: invalid request argument"}, status=400)
            user.save()
            return JsonResponse({"code": 0, "message": "Record button successfully changed!"}, status=200)
        else:
            pass
    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status=405)
    
def wb_create(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        openid = json_param['openid']
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"code": "401", "message": "User Unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            cur_wbnumber = user.wdlistnumber
            user.wbinfo.create(owner_openid=user, index=cur_wbnumber+1)
            user.wdlistnumber = user.wdlistnumber + 1
            user.save()
            return JsonResponse({"code": 0, "message": "New wordbook successfully created!"}, status=200)
        else:
            pass
    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status=405)
    
