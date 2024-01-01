from django.http import JsonResponse
from django.http import FileResponse
from app.mywrapper import followlist, timeover
from app import models


def friends_namesearch(request, json_param, user):
    f_name = json_param['name']
    openid = json_param['openid']
    f_list = models.user.objects.filter(nickname=f_name)     # 查找用户
    if len(f_list) == 0:
        return JsonResponse({"message": "User not found"}, status=404)
    else:
        f_list_info = []
        cur_list = followlist(user.followee)
        for xuser in f_list:
            if xuser.open_id == openid:     # 自己，跳过
                continue
            f_info = []
            f_info.append(xuser.uid)
            f_info.append(xuser.nickname)
            f_info.append(xuser.headicon_name)
            if xuser.uid in cur_list:     # 是否关注该用户
                f_info.append(1)
            else:
                f_info.append(0)
            f_list_info.append(f_info)
        return JsonResponse({'result': f_list_info}, status=200)


def friends_uidsearch(request, json_param, user):
    f_uid = int(json_param['uid'])
    openid = json_param['openid']
    f_list = models.user.objects.filter(uid=f_uid)
    if len(f_list) == 0:
        return JsonResponse({"message": "User not found"}, status=404)
    elif len(f_list) == 1:
        f_user = f_list[0]
        f_info = []
        if f_user.open_id != openid:     # 不是自己
            f_info_content = []
            f_info_content.append(f_user.uid)
            f_info_content.append(f_user.nickname)
            f_info_content.append(f_user.headicon_name)
            cur_flist = followlist(user.followee)     # 获取当前关注列表
            if f_uid in cur_flist:     # 是否关注该用户
                f_info_content.append(1)
            else:
                f_info_content.append(0)
            f_info.append(f_info_content)
        return JsonResponse({'result': f_info}, status=200)
    else:
        return JsonResponse({'message': 'Duplicate users'}, status=403)


def friends_list(request, json_param, user):
    f_list = followlist(user.followee)
    true_f_list = []
    f_info_list = []
    for x in f_list:
        f_uid = x
        f_userlist = models.user.objects.filter(uid=f_uid)     # 获取用户
        if len(f_userlist) == 1:
            f_user = f_userlist[0]
            f_info = []
            f_info.append(f_user.uid)
            f_info.append(f_user.nickname)
            f_info.append(f_user.headicon_name)
            f_info_list.append(f_info)
            true_f_list.append(x)
    user.followee = str(true_f_list)     # 将关注列表返存
    user.save()
    return JsonResponse({'result': f_info_list}, status=200)


def friends_follow(request, json_param, user, f_user):
    f_uid = json_param['uid']
    f_curlist = followlist(user.followee)
    if f_uid in f_curlist:
        return JsonResponse({"message": "Already followed"}, status=403)
    else:
        f_curlist.append(f_uid)     # 添加关注
        user.followee = str(f_curlist)     # 关注列表写回
        user.save()
        return JsonResponse({"message": "successfully follow"}, status=200)


def friends_unfollow(request, json_param, user, f_user):
    f_uid = json_param['uid']
    f_curlist = followlist(user.followee)
    if f_uid in f_curlist:     # 是关注者
        f_curlist.remove(f_uid)     # 移除关注
        user.followee = str(f_curlist)
        user.save()
        return JsonResponse({"message": "successfully unfollow"}, status=200)
    else:
        return JsonResponse({"message": "Not followed"}, status=403)


def friends_headicon(request, json_param, user, f_user):
    image = f_user.headicon
    return FileResponse(image, as_attachment=True,
                        filename=f_user.headicon_name, status=200)


def friends_info(request, json_param, user, f_user):
    f_uid = json_param['uid']
    cur_list = followlist(user.followee)
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


def friends_subscribe(request, json_param, user, f_user, f_wb):
    user_flwblist = user.flwbs.filter(wb_info=f_wb)
    if len(user_flwblist) == 0:
        user.flwbs.create(wb_info=f_wb)     # 订阅单词本
        return JsonResponse({"message": "successfully subscribe"}, status=200)
    elif len(user_flwblist) == 1:
        return JsonResponse({'mseeage': "Already followed"}, status=403)
    else:
        for x in user_flwblist:
            x.delete()
        user.flwbs.create(wb_info=f_wb)
        return JsonResponse({'message': 'Duplicate wordbooks'}, status=403)


def friends_unsubscribe(request, json_param, user, f_user, f_wb):
    user_flwblist = user.flwbs.filter(wb_info=f_wb)
    if len(user_flwblist) == 1:
        user_flwblist[0].delete()     # 取消订阅
        return JsonResponse(
            {"message": "successfully unsubscribe"}, status=200)
    elif len(user_flwblist) == 0:
        return JsonResponse({"message": "Wordbook not subscribed"}, status=403)
    else:
        for x in user_flwblist:
            x.delete()
        return JsonResponse({'message': 'Duplicate wordbooks'}, status=403)


def friends_wbcover(request, json_param, user, f_user, f_wb):
    image = f_wb.image
    return FileResponse(image, as_attachment=True,
                        filename=f_wb.image_name, status=200)
