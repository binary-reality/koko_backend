from django.http import JsonResponse
from functools import wraps

import json
from app import models


def paramcheck(param_json: dict, key: str, dest: type):
    """检查参数存在性与类型正确性函数

    Args:
        param_json (dict): 待检查的参数所在的字典
        key (str): 待检查的键值
        dest (type): 待检查的目标类型

    Returns:
        bool: 正确，True
        str: 错误，返回报错信息
    """
    if key in param_json:
        if isinstance(param_json[key], dest):
            return True
        else:
            print('Request key type error')
            return 'Request key type error'
    else:
        print('Request key missing')
        return 'Request key missing'


def paramcheck_file(request, key: str, dest: type):
    """这是直接根据请求来进行参数检查的函数

    Args:
        request : 请求
        key (str): 待检查的键值
        dest (type): 待检查的目标类型

    Returns:
        bool: 正确，True
        str: 错误，返回报错信息
    """
    value = request.POST.get(key)
    print(key)
    print(type(value))
    if value is None:
        print('Request key missing')
        return 'Request key missing'
    if not isinstance(value, dest):
        print('Request key type error')
        return 'Request key type error'
    return True


def followlist(followee: str):
    """根据字符串返回关注者的uid列表

    Args:
        followee (str): 关注者uid列表的字符串形式

    Returns:
        list: 关注者uid列表
    """
    followeelist = followee.strip('[').strip(']').split(',')
    reslist = []
    if followeelist == ['']:
        return reslist
    for x in followeelist:
        reslist.append(int(x))
    return reslist


def timeover(recDate):
    """判断某一记录时间是否合法（一年之内）

    Args:
        recDate (Date): 记录时间

    Returns:
        bool: True 合法
              False 不合法
    """
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
    """
    @apiDefine wrapper_normal_error
    @apiError {String} message 错误信息
    @apiErrorExample {json} 请求方式错误
        HTTP/1.1 405 Method Not Allowed
        {
            "message": "Method not allowed"
        }
    @apiErrorExample {json} 存在非唯一用户
        HTTP/1.1 403 Forbidden
        {
            "message": "Duplicate users"
        }
    @apiErrorExample {json} 发出请求的用户不存在
        HTTP/1.1 401 Unauthorized
        {
            "message": "User unauthorized"
        }
    @apiErrorExample {json} 请求中出现参数缺失
        HTTP/1.1 400 Bad Request
        {
            "message": "Request key missing"
        }
    @apiErrorExample {json} 请求中出现参数类型错误
        HTTP/1.1 400 Bad Request
        {
            "message": "Request key type error"
        }
    """
    @wraps(function)
    def wrapper(request):
        if request.method == "POST":
            json_param = json.loads(request.body)
            checkbit = paramcheck(json_param, 'openid', str)     # 检查参数类型
            if isinstance(checkbit, bool):
                user_id = json_param['openid']
            else:
                return JsonResponse({'message': checkbit}, status=400)     # 检查时报失败
            userlist = models.user.objects.filter(open_id=user_id)
            if len(userlist) == 0:
                return JsonResponse(
                    {"message": "User unauthorized"}, status=401)
            elif len(userlist) == 1:
                return function(request, json_param, userlist[0])
            else:
                return JsonResponse({'message': 'Duplicate users'}, status=403)
        else:
            return JsonResponse({"message": "Method not allowed"}, status=405)
    return wrapper


def wrapper_file(function):
    @wraps(function)
    def wrapper(request):
        if request.method == "POST":
            checkbit = paramcheck_file(request, 'openid', str)
            if isinstance(checkbit, bool):
                user_id = request.POST.get('openid')
            else:
                return JsonResponse({'message': checkbit}, status=400)
            userlist = models.user.objects.filter(open_id=user_id)
            if len(userlist) == 0:
                return JsonResponse(
                    {"message": "User unauthorized"}, status=401)
            elif len(userlist) == 1:
                return function(request, userlist[0])
            else:
                return JsonResponse({'message': 'Duplicate users'}, status=403)
        else:
            return JsonResponse({"message": "Method not allowed"}, status=405)
    return wrapper


def wrapper_wb(function):
    """
    @apiDefine wrapper_wb_error
    @apiUse wrapper_normal_error
    @apiErrorExample {json} 存在同一用户同一单词本序号非唯一单词本
        HTTP/1.1 403 Forbidden
        {
            "message": "Duplicate wordbooks"
        }
    @apiErrorExample {json} 请求的单词本不存在
        HTTP/1.1 404 Not Found
        {
            "message": "Wordbook not found"
        }
    """
    @wraps(function)
    @wrapper_normal
    def wrapper(request, json_param, user):
        checkbit = paramcheck(json_param, 'index', int)
        if isinstance(checkbit, bool):
            wbindex = json_param['index']
        else:
            return JsonResponse({'message': checkbit}, status=400)
        wblist = user.wbinfo.filter(index=wbindex)
        if len(wblist) == 0:
            return JsonResponse({"message": "Wordbook not found"}, status=404)
        elif len(wblist) == 1:
            return function(request, json_param, user, wblist[0])
        else:
            return JsonResponse({'message': 'Duplicate wordbooks'}, status=403)
    return wrapper


def wrapper_wb_file(function):
    @wraps(function)
    @wrapper_file
    def wrapper(request, user):
        checkbit = paramcheck_file(request, 'index', str)
        if isinstance(checkbit, bool):
            wbindex = request.POST.get('index')
        else:
            return JsonResponse({'message': checkbit}, status=400)
        wbindex = int(wbindex)
        wblist = user.wbinfo.filter(index=wbindex)
        if len(wblist) == 0:
            return JsonResponse({"message": "Wordbook not found"}, status=404)
        elif len(wblist) == 1:
            return function(request, user, wblist[0])
        else:
            return JsonResponse({'message': 'Duplicate wordbooks'}, status=403)
    return wrapper


def wrapper_friends(function):
    """
    @apiDefine wrapper_friends_error
    @apiUse wrapper_normal_error
    @apiErrorExample {json} 存在同一uid非唯一用户
        HTTP/1.1 403 Forbidden
        {
            "message": "Duplicate users"
        }
    @apiErrorExample {json} 请求的其他用户不存在
        HTTP/1.1 404 Not Found
        {
            "message": "User not found"
        }
    """
    @wraps(function)
    @wrapper_normal
    def wrapper(request, json_param, user):
        checkbit = paramcheck(json_param, 'uid', int)
        if isinstance(checkbit, bool):
            f_uid = json_param['uid']
        else:
            return JsonResponse({'message': checkbit}, status=400)
        f_list = models.user.objects.filter(uid=f_uid)
        if len(f_list) == 0:
            return JsonResponse({"message": "User not found"}, status=404)
        elif len(f_list) == 1:
            return function(request, json_param, user, f_list[0])
        else:
            return JsonResponse({'message': 'Duplicate users'}, status=403)
    return wrapper


def wrapper_friends_wb(function):
    """
    @apiDefine wrapper_friends_wb_error
    @apiUse wrapper_friends_error
    @apiErrorExample {json} 存在同一用户同一单词本序号非唯一单词本
        HTTP/1.1 403 Forbidden
        {
            "message": "Duplicate wordbooks"
        }
    @apiErrorExample {json} 请求的单词本不存在
        HTTP/1.1 404 Not Found
        {
            "message": "Wordbook not found"
        }
    """
    @wraps(function)
    @wrapper_friends
    def wrapper(request, json_param, user, f_user):
        checkbit = paramcheck(json_param, 'id', int)
        if isinstance(checkbit, bool):
            f_wbid = json_param['id']
        else:
            return JsonResponse({'message': checkbit}, status=400)
        f_wblist = f_user.wbinfo.filter(index=f_wbid)
        if len(f_wblist) == 0:
            return JsonResponse({"message": "Wordbook not found"}, status=404)
        elif len(f_wblist) == 1:
            return function(request, json_param, user, f_user, f_wblist[0])
        else:
            return JsonResponse({'message': 'Duplicate wordbooks'}, status=403)
    return wrapper
