from django.http import JsonResponse
from django.http import FileResponse
from django.views.decorators.csrf import csrf_exempt

import json, os
from app import models, mywapper
from app.mywapper import paramcheck, timeover, followlist
from koko import settings

# Create your views here.

@csrf_exempt
def login(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        checkbit = paramcheck(json_param, 'code', str)
        if type(checkbit) == bool:
            from app.func import login
            return login.login(request, json_param)
        else:
            return JsonResponse({'message': checkbit}, status=400)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
@mywapper.wapper_normal
def getlogheadicon(request, json_param, user):
    from app.func import login
    return login.getlogheadicon(request, json_param, user)

@csrf_exempt
@mywapper.wapper_normal
def read(request, json_param, user):
    checkbit = paramcheck(json_param, 'wave', str)
    if type(checkbit) != bool:
        return JsonResponse({'message': checkbit}, status=400)
    checkbit = paramcheck(json_param, 'word', str)
    if type(checkbit) != bool:
        return JsonResponse({'message': checkbit}, status=400)
    from app.func import read
    return read.read(request, json_param, user)
    
@csrf_exempt
@mywapper.wapper_normal
def search(request, json_param, user):
    checkbit = paramcheck(json_param, 'searchWord', str)
    if type(checkbit) == bool:
        from app.func import read
        return read.search(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)
    
@csrf_exempt
@mywapper.wapper_normal
def detail(request, json_param, user):
    checkbit = paramcheck(json_param, 'word', str)
    if type(checkbit) == bool:
        from app.func import read
        return read.detail(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)
    
@csrf_exempt
@mywapper.wapper_normal
def getlist(request, json_param, user):
    checkbit = paramcheck(json_param, 'type', int)
    if type(checkbit) == bool:
        from app.func import read
        return read.getlist(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywapper.wapper_normal
def headicon_change(request, json_param, user):
    checkbit = paramcheck(json_param, 'name', str)
    if type(checkbit) == bool:
        from app.func import setting
        return setting.headicon_change(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywapper.wapper_normal
def nickname_change(request, json_param, user):
    checkbit = paramcheck(json_param, 'nickname', str)
    if type(checkbit) == bool:
        from app.func import setting
        return setting.nickname_change(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywapper.wapper_normal
def timeline_change(request, json_param, user):
    checkbit = paramcheck(json_param, 'timeline', int)
    if type(checkbit) == bool:
        from app.func import setting
        return setting.timeline_change(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywapper.wapper_normal
def record_change(request, json_param, user):
    checkbit = paramcheck(json_param, 'recordOn', str)
    if type(checkbit) == bool:
        from app.func import setting
        return setting.record_change(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywapper.wapper_normal
def wb_create(request, json_param, user):
    from app.func import wb
    return wb.wb_create(request, json_param, user)

@csrf_exempt
@mywapper.wapper_wb
def wb_info_change(request, json_param, user, user_wb):
    checkbit = paramcheck(json_param, 'name', str)
    if type(checkbit) != bool:
        return JsonResponse({'message': checkbit}, status=400)
    checkbit = paramcheck(json_param, 'intro', str)
    if type(checkbit) == bool:
        from app.func import wb
        return wb.wb_info_change(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywapper.wapper_wb
def wb_image_get(request, json_param, user, user_wb):
    from app.func import wb
    return wb.wb_image_get(request, json_param, user, user_wb)

@csrf_exempt
@mywapper.wapper_wb
def wb_image_set(request, json_param, user, user_wb):
    checkbit = paramcheck(json_param, 'name', str)
    if type(checkbit) == bool:
        from app.func import wb
        return wb.wb_image_set(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywapper.wapper_wb
def wb_remove(request, json_param, user, user_wb):
    from app.func import wb
    return wb.wb_remove(request, json_param, user, user_wb)

@csrf_exempt
@mywapper.wapper_wb
def wb_type(request, json_param, user, user_wb):
    checkbit = paramcheck(json_param, 'type', int)
    if type(checkbit) == bool:
        from app.func import wb
        return wb.wb_type(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywapper.wapper_wb
def word_add(request, json_param, user, user_wb):
    checkbit = paramcheck(json_param, 'word', str)
    if type(checkbit) == bool:
        from app.func import word
        return word.word_add(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywapper.wapper_wb
def word_remove(request, json_param, user, user_wb):
    checkbit = paramcheck(json_param, 'word', str)
    if type(checkbit) == bool:
        from app.func import word
        return word.word_remove(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywapper.wapper_normal
def friends_namesearch(request, json_param, user):
    checkbit = paramcheck(json_param, 'name', str)
    if type(checkbit) == bool:
        from app.func import friends
        return friends.friends_namesearch(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
def friends_uidsearch(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        checkbit = paramcheck(json_param, 'openid', str)
        if type(checkbit) == bool:
            openid = json_param["openid"]
        else:
            return JsonResponse({'message': checkbit}, status=400)
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"message": "User unauthorized"}, status=401)
        elif len(userlist) == 1:
            checkbit = paramcheck(json_param, 'uid', str)
            if type(checkbit) == bool:
                f_uid = int(json_param['uid'])
            else:
                return JsonResponse({'message': checkbit}, status=400)
            f_list = models.user.objects.filter(uid=f_uid)
            if len(f_list) == 0:
                return JsonResponse({"message": "User not found"}, status=404)
            elif len(f_list) == 1:
                f_user = f_list[0]
                f_info = []
                if f_user.open_id != openid:
                    f_info_content = []
                    f_info_content.append(f_user.uid)
                    f_info_content.append(f_user.nickname)
                    f_info_content.append(f_user.headicon_name)
                    cur_flist = followlist(userlist[0].followee)
                    if f_uid in cur_flist:
                        f_info_content.append(1)
                    else:
                        f_info_content.append(0)
                    f_info.append(f_info_content)
                return JsonResponse({'result': f_info}, status=200)
            else:
                pass
        else:
            pass
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def friends_list(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        checkbit = paramcheck(json_param, 'openid', str)
        if type(checkbit) == bool:
            openid = json_param["openid"]
        else:
            return JsonResponse({'message': checkbit}, status=400)
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"message": "User unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            f_list = followlist(user.followee)
            true_f_list = []
            f_info_list = []
            for x in f_list:
                f_uid = x
                f_userlist = models.user.objects.filter(uid=f_uid)
                if len(f_userlist) == 1:
                    f_user = f_userlist[0]
                    f_info = []
                    f_info.append(f_user.uid)
                    f_info.append(f_user.nickname)
                    f_info.append(f_user.headicon_name)
                    f_info_list.append(f_info)
                    true_f_list.append(x)
            user.followee = str(true_f_list)
            user.save()
            return JsonResponse({'result': f_info_list}, status=200)
        else:
            pass
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
      
@csrf_exempt
def friends_follow(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        checkbit = paramcheck(json_param, 'openid', str)
        if type(checkbit) == bool:
            openid = json_param["openid"]
        else:
            return JsonResponse({'message': checkbit}, status=400)
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"message": "User unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            checkbit = paramcheck(json_param, 'uid', int)
            if type(checkbit) == bool:
                f_uid = json_param['uid']
            else:
                return JsonResponse({'message': checkbit}, status=400)
            f_userlist = models.user.objects.filter(uid=f_uid)
            if len(f_userlist) == 1:
                f_curlist = followlist(user.followee)
                if f_uid in f_curlist:
                    return JsonResponse({"message": "Already followed"}, status=200)
                else:
                    f_curlist.append(f_uid)
                    user.followee = str(f_curlist)
                    user.save()
                    return JsonResponse({"message": "successfully follow"}, status=200)
            elif len(f_userlist) == 0:
                return JsonResponse({"message": "User not found"}, status=406)
            else:
                pass
        else:
            pass
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def friends_unfollow(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        checkbit = paramcheck(json_param, 'openid', str)
        if type(checkbit) == bool:
            openid = json_param["openid"]
        else:
            return JsonResponse({'message': checkbit}, status=400)
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"message": "User unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            checkbit = paramcheck(json_param, 'uid', int)
            if type(checkbit) == bool:
                f_uid = json_param['uid']
            else:
                return JsonResponse({'message': checkbit}, status=400)
            f_userlist = models.user.objects.filter(uid=f_uid)
            if len(f_userlist) == 1:
                f_curlist = followlist(user.followee)
                if f_uid in f_curlist:
                    f_curlist.remove(f_uid)
                    user.followee = str(f_curlist)
                    user.save()
                    return JsonResponse({"message": "successfully unfollow"}, status=200)
                else:
                    return JsonResponse({"message": "Not followed"}, status=200)
                    
            elif len(f_userlist) == 0:
                return JsonResponse({"message": "User not found"}, status=406)
            else:
                pass
        else:
            pass
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
@csrf_exempt
def friends_headicon(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        checkbit = paramcheck(json_param, 'openid', str)
        if type(checkbit) == bool:
            openid = json_param["openid"]
        else:
            return JsonResponse({'message': checkbit}, status=400)
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"message": "User unauthorized"}, status=401)
        elif len(userlist) == 1:
            checkbit = paramcheck(json_param, 'uid', int)
            if type(checkbit) == bool:
                f_uid = json_param['uid']
            else:
                return JsonResponse({'message': checkbit}, status=400)
            f_userlist = models.user.objects.filter(uid=f_uid)
            if len(f_userlist) == 1:
                image = f_userlist[0].headicon
                return FileResponse(image, as_attachment=True, filename=f_userlist[0].headicon_name, status=200)
                    
            elif len(f_userlist) == 0:
                return JsonResponse({"message": "User not found"}, status=406)
            else:
                pass
        else:
            pass
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
@csrf_exempt
def friends_info(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        checkbit = paramcheck(json_param, 'openid', str)
        if type(checkbit) == bool:
            openid = json_param["openid"]
        else:
            return JsonResponse({'message': checkbit}, status=400)
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"message": "User unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            checkbit = paramcheck(json_param, 'uid', int)
            if type(checkbit) == bool:
                f_uid = json_param['uid']
            else:
                return JsonResponse({'message': checkbit}, status=400)
            f_userlist = models.user.objects.filter(uid=f_uid)
            if len(f_userlist) == 1:
                cur_list = followlist(user.followee)
                f_user = f_userlist[0]
                user_data = {}
                # info
                user_data_info = {}
                user_data_info['nickname'] = f_user.nickname
                if f_uid in cur_list:
                    user_data_info['following'] = 1
                else:
                    user_data_info['following'] = 0
                user_data['info'] = user_data_info

                # wordbooks
                fl_id = []
                user_flwbs_list = user.flwbs.all()
                for flwb in user_flwbs_list:
                    if flwb.wb_info.owner_openid.uid == f_uid:
                        fl_id.append(flwb.wb_info.index)
                user_data_wdbks = []
                f_user_wbinfo = f_user.wbinfo.all()
            
                for i in range(1, f_user.wdlistnumber + 1):
                    wd_content = {}
                    cur_info = f_user_wbinfo.get(index=i)
                    wd_content['id'] = i
                    wd_content['uid'] = cur_info.owner_openid.uid
                    wd_content['name'] = cur_info.name
                    wd_content['intro'] = cur_info.intro
                    wd_content['coverUrl'] = cur_info.image_name
                    wd_content['type'] = cur_info.public_ctrl
                    if i in fl_id:
                        wd_content['following'] = 1
                    else:
                        wd_content['following'] = 0
                    words = []
                    wdlist = cur_info.wordlist.all()
                    for x in wdlist:
                        words.append(x.content)
                    wd_content['words'] = words
                    user_data_wdbks.append(wd_content)
                user_data['wordbooks'] = user_data_wdbks

                # readHistory
                f_rdHis = []
                f_user_rdHis = f_user.readingrecord.all()
                for x in f_user_rdHis:
                    if timeover(x.date):
                        x.delete()
                    else:
                        record = []
                        record.append(x.content)
                        record.append(x.date)
                        record.append(x.lastrd)
                        record.append(x.lastres)
                        f_rdHis.append(record)
                user_data['readHistory'] = f_rdHis

                return JsonResponse({"detail": user_data}, status=200)
                    
            elif len(f_userlist) == 0:
                return JsonResponse({"message": "User not found"}, status=406)
            else:
                pass
        else:
            pass
    else:
        return JsonResponse({"code": "405", "message": "Method not allowed"}, status=405)

@csrf_exempt
def friends_subscribe(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        checkbit = paramcheck(json_param, 'openid', str)
        if type(checkbit) == bool:
            openid = json_param["openid"]
        else:
            return JsonResponse({'message': checkbit}, status=400)
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"message": "User unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            checkbit = paramcheck(json_param, 'uid', int)
            if type(checkbit) == bool:
                f_uid = json_param['uid']
            else:
                return JsonResponse({'message': checkbit}, status=400)
            f_userlist = models.user.objects.filter(uid=f_uid)
            if len(f_userlist) == 1:
                cur_list = followlist(user.followee)
                if f_uid in cur_list:
                    f_user = f_userlist[0]
                    checkbit = paramcheck(json_param, 'id', int)
                    if type(checkbit) == bool:
                        f_wbid = json_param['id']
                    else:
                        return JsonResponse({'message': checkbit}, status=400)
                    f_wblist = f_user.wbinfo.filter(index=f_wbid)
                    if len(f_wblist) == 1:
                        f_wbinfo = f_wblist[0]
                        f_wblist = user.flwbs.filter(wb_info=f_wbinfo)
                        if len(f_wblist) == 0:
                            user.flwbs.create(wb_info=f_wbinfo)
                            return JsonResponse({"message": "successfully subscribe"}, status=200)
                        elif len(f_wblist) == 1:
                            return JsonResponse({'mseeage': "Already followed"}, status=200)
                        else:
                            pass
                    elif len(f_wblist) == 0:
                        return JsonResponse({"message": "Wordbook not found"}, status=404)
                    else:
                        pass
                else:
                    return JsonResponse({"message": "Not followed"}, status=406)
                    
            elif len(f_userlist) == 0:
                return JsonResponse({"message": "User not found"}, status=404)
            else:
                pass
        else:
            pass
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)
    
@csrf_exempt
def friends_unsubscribe(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        checkbit = paramcheck(json_param, 'openid', str)
        if type(checkbit) == bool:
            openid = json_param["openid"]
        else:
            return JsonResponse({'message': checkbit}, status=400)
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"message": "User unauthorized"}, status=401)
        elif len(userlist) == 1:
            user = userlist[0]
            checkbit = paramcheck(json_param, 'uid', int)
            if type(checkbit) == bool:
                f_uid = json_param['uid']
            else:
                return JsonResponse({'message': checkbit}, status=400)
            f_userlist = models.user.objects.filter(uid=f_uid)
            if len(f_userlist) == 1:
                cur_list = followlist(user.followee)
                if f_uid in cur_list:
                    f_user = f_userlist[0]
                    checkbit = paramcheck(json_param, 'id', int)
                    if type(checkbit) == bool:
                        f_wbid = json_param['id']
                    else:
                        return JsonResponse({'message': checkbit}, status=400)
                    f_wblist = f_user.wbinfo.filter(index=f_wbid)
                    if len(f_wblist) == 1:
                        f_wbinfo = f_wblist[0]
                        user_flwb_list = user.flwbs.filter(wb_info=f_wbinfo)
                        if len(user_flwb_list) == 1:
                            user_flwb_list[0].delete()
                            return JsonResponse({"message": "successfully unsubscribe"}, status=200)
                        elif len(user_flwb_list) == 0:
                            return JsonResponse({"message": "Wordbook not subscribed"}, status=406)
                        else:
                            pass
                    elif len(f_wblist) == 0:
                        return JsonResponse({"message": "Wordbook not found"}, status=404)
                    else:
                        pass
                else:
                    return JsonResponse({"message": "Not followed"}, status=406)
                    
            elif len(f_userlist) == 0:
                return JsonResponse({"message": "User not found"}, status=404)
            else:
                pass
        else:
            pass
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)

@csrf_exempt
def friends_wbcover(request):
    if request.method == "POST":
        json_param = json.loads(request.body)
        print(json_param)
        checkbit = paramcheck(json_param, 'openid', str)
        if type(checkbit) == bool:
            openid = json_param["openid"]
        else:
            return JsonResponse({'message': checkbit}, status=400)
        userlist = models.user.objects.filter(open_id=openid)
        if len(userlist) == 0:
            return JsonResponse({"message": "User unauthorized"}, status=401)
        elif len(userlist) == 1:
            checkbit = paramcheck(json_param, 'uid', int)
            if type(checkbit) == bool:
                f_uid = json_param['uid']
            else:
                return JsonResponse({'message': checkbit}, status=400)
            f_userlist = models.user.objects.filter(uid=f_uid)
            if len(f_userlist) == 1:
                checkbit = paramcheck(json_param, 'id', int)
                if type(checkbit) == bool:
                    f_wbid = json_param['id']
                else:
                    return JsonResponse({'message': checkbit}, status=400)
                f_user = f_userlist[0]
                f_wblist = f_user.wbinfo.filter(index=f_wbid)
                if len(f_wblist) == 1:
                    f_wb = f_wblist[0]
                    image = f_wb.image
                    return FileResponse(image, as_attachment=True, filename=f_wb.image_name, status=200)
                elif len(f_wblist) == 0:
                    return JsonResponse({"message": "Wordbook not found"}, status=404)
                else:
                    pass
            elif len(f_userlist) == 0:
                return JsonResponse({"message": "User not found"}, status=404)
            else:
                pass
        else:
            pass
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)