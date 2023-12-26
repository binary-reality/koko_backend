from django.http import JsonResponse
from functools import wraps

import json
from app import models

def paramcheck(param_json: dict, key: str, dest: type):
    if key in param_json:
        if type(param_json[key]) == dest:
            return True
        else:
            print('Request key type error')
            return 'Request key type error'
    else:
        print('Request key missing')
        return 'Request key missing'
    
def followlist(followee: str):
    followeelist = followee.strip('[').strip(']').split(',')
    reslist = []
    if followeelist == ['']:
        return reslist
    for x in followeelist:
        reslist.append(int(x))
    return reslist

def timeover(recDate):
    import time
    t = time.localtime()
    (y, m, d) = (t.tm_year, t.tm_mon, t.tm_mday)
    recy = recDate.year
    recm = recDate.month
    recd = recDate.day
    if y - recy > 1:
        return True
    elif y == recy:
        return False
    else:
        if recm < m:
            return True
        elif recm > m:
            return False
        else:
            if recd >= d:
                return False
            else:
                return True

def wrapper_normal(function):
    @wraps(function)
    def wrapper(request):
        if request.method == "POST":
            json_param = json.loads(request.body)
            checkbit = paramcheck(json_param, 'openid', str)
            if type(checkbit) == bool:
                user_id = json_param['openid']
            else:
                return JsonResponse({'message': checkbit}, status=400)
            userlist = models.user.objects.filter(open_id=user_id)
            if len(userlist) == 0:
                return JsonResponse({"message": "User unauthorized"}, status=401)
            elif len(userlist) == 1:
                return function(request, json_param, userlist[0])
            else:
                return JsonResponse({'message': 'Duplicate users'}, status=401)
        else:
            return JsonResponse({"message": "Method not allowed"}, status=405)
    return wrapper

def wrapper_wb(function):
    @wraps(function)
    @wrapper_normal
    def wrapper(request, json_param, user):
        checkbit = paramcheck(json_param, 'index', int)
        if type(checkbit) == bool:
            wbindex = json_param['index']
        else:
            return JsonResponse({'message': checkbit}, status=400)
        wblist = user.wbinfo.filter(index=wbindex)
        if len(wblist) == 0:
            return JsonResponse({"message": "Wordbook not found"}, status=404)
        elif len(wblist) == 1:
            return function(request, json_param, user, wblist[0])
        else:
            return JsonResponse({'message': 'Duplicate wordbook'}, status=401)
    return wrapper

def wrapper_friends(function):
    @wraps(function)
    @wrapper_normal
    def wa