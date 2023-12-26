from django.http import JsonResponse
from django.http import FileResponse

import json
import requests

from app.mywrapper import followlist, timeover
from app import models

def login(request, json_param):

    code = json_param['code']
    login_response = requests.get(
            url = "https://api.weixin.qq.com/sns/jscode2session",
            params = {
                "appid": "wx5ef6067498a5d631",
                "secret": "f72baea608e953e3d5850999d9667309",
                "js_code": code,
                "grant_type": "authorization_code"
            }
    )
    response_json = json.loads(login_response.text)
    if 'errcode' in response_json:
        pass
    else:
        response_json['errcode'] = 0
    if response_json['errcode'] == 0:
        user_id = response_json['openid']
        del response_json['session_key']
        valid_user_list = models.user.objects.filter(open_id=user_id)
        if len(valid_user_list) == 0:
            models.user.objects.create(open_id=user_id, nickname="用户"+user_id, followee='[]')
        curuser = models.user.objects.get(open_id=user_id)
        user_data = {}

        # file
        user_data['file'] = curuser.headicon_name
        # info
        user_data_info = {}
        user_data_info['openid'] = curuser.open_id
        user_data_info['uid'] = curuser.uid
        user_data_info['nickname'] = curuser.nickname
        user_data_info['timeline'] = curuser.reserved_time
        user_data_info['followees'] = followlist(curuser.followee)
        if curuser.read_keep == 1:
            user_data_info['recordOn'] = 'true'
        else:
            user_data_info['recordOn'] = 'false'
        user_data_info['wbnum'] = curuser.wdlistnumber
        user_data['info'] = user_data_info

        # follow wordbooks
        user_data_flwbs = []
        curuser_flwbs = curuser.flwbs.all()
        for flwb in curuser_flwbs:
            flwb_content = {}
            flwb_info = flwb.wb_info
            flwb_content['name'] = flwb_info.name
            flwb_content['intro'] = flwb_info.intro
            flwb_content['coverUrl'] = flwb_info.image_name
            flwb_content['id'] = flwb_info.index
            flwb_content['uid'] = flwb_info.owner_openid.uid
            flwb_content['following'] = 1
            words = []
            wdlist = flwb_info.wordlist.all()
            for x in wdlist:
                words.append(x.content)
            flwb_content['words'] = words
            user_data_flwbs.append(flwb_content)
        user_data['flwbs'] = user_data_flwbs
            
        # wordbooks
        user_data_wdbks = []
        curuser_wbinfo = curuser.wbinfo.all()
            
        for i in range(1, curuser.wdlistnumber + 1):
            wd_content = {}
            cur_info = curuser_wbinfo.get(index=i)
            wd_content['id'] = i
            wd_content['name'] = cur_info.name
            wd_content['intro'] = cur_info.intro
            wd_content['coverUrl'] = cur_info.image_name
            wd_content['type'] = cur_info.public_ctrl
            words = []
            wdlist = cur_info.wordlist.all()
            for x in wdlist:
                words.append(x.content)
            wd_content['words'] = words
            user_data_wdbks.append(wd_content)
        user_data['wordbooks'] = user_data_wdbks

        # wordHistory
        wdHis = []
        curuser_his = curuser.searchrecord.all()
        for x in curuser_his:
            if timeover(x.date):
                x.delete()
            else:
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
            if timeover(x.date):
                x.delete()
            else:
                record = []
                record.append(x.content)
                record.append(x.date)
                record.append(x.lastrd)
                record.append(x.lastres)
                rdHis.append(record)
        user_data['readHistory'] = rdHis
        response_json['user_data'] = user_data
    return JsonResponse(response_json, status=200)

def getlogheadicon(request, json_param, user):
    image = user.headicon
    return FileResponse(image, as_attachment=True, filename="headicon.jpg", status=200)