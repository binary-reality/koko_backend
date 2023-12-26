from django.http import JsonResponse

from app.mywapper import followlist
from app import models

def friends_namesearch(request, json_param, user):
    f_name = json_param['name']
    openid = json_param['openid']
    f_list = models.user.objects.filter(nickname=f_name)
    if len(f_list) == 0:
        return JsonResponse({"message": "User not found"}, status=404)
    else:
        f_list_info = []
        cur_list = followlist(user.followee)
        for xuser in f_list:
            if xuser.open_id == openid:
                continue
            f_info = []
            f_info.append(xuser.uid)
            f_info.append(xuser.nickname)
            f_info.append(xuser.headicon_name)
            if xuser.uid in cur_list:
                f_info.append(1)
            else:
                f_info.append(0)
            f_list_info.append(f_info)
        return JsonResponse({'result': f_list_info}, status=200)