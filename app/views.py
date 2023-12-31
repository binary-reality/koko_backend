from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json, os
from app import models, mywrapper
from app.mywrapper import paramcheck, paramcheck_file
from koko import settings

# Create your views here.

@csrf_exempt
def hello(request):
    return HttpResponse("Welcome to koko!", status=200)

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
@mywrapper.wrapper_normal
def getlogheadicon(request, json_param, user):
    from app.func import login
    return login.getlogheadicon(request, json_param, user)

@csrf_exempt
@mywrapper.wrapper_file
def read(request, user):
    checkbit = paramcheck_file(request, 'wave', str)
    if type(checkbit) != bool:
        return JsonResponse({'message': checkbit}, status=400)
    checkbit = paramcheck_file(request, 'word', str)
    if type(checkbit) != bool:
        return JsonResponse({'message': checkbit}, status=400)
    from app.func import read
    return read.read(request, user)
    
@csrf_exempt
@mywrapper.wrapper_normal
def search(request, json_param, user):
    checkbit = paramcheck(json_param, 'searchWord', str)
    if type(checkbit) == bool:
        from app.func import read
        return read.search(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)
    
@csrf_exempt
@mywrapper.wrapper_normal
def detail(request, json_param, user):
    checkbit = paramcheck(json_param, 'word', str)
    if type(checkbit) == bool:
        from app.func import read
        return read.detail(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)
    
@csrf_exempt
@mywrapper.wrapper_normal
def getlist(request, json_param, user):
    checkbit = paramcheck(json_param, 'type', int)
    if type(checkbit) == bool:
        from app.func import read
        return read.getlist(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_file
def headicon_change(request, user):
    checkbit = paramcheck_file(request, 'name', str)
    if type(checkbit) == bool:
        from app.func import setting
        return setting.headicon_change(request, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_normal
def nickname_change(request, json_param, user):
    checkbit = paramcheck(json_param, 'nickname', str)
    if type(checkbit) == bool:
        from app.func import setting
        return setting.nickname_change(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_normal
def timeline_change(request, json_param, user):
    checkbit = paramcheck(json_param, 'timeline', int)
    if type(checkbit) == bool:
        from app.func import setting
        return setting.timeline_change(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_normal
def record_change(request, json_param, user):
    checkbit = paramcheck(json_param, 'recordOn', str)
    if type(checkbit) == bool:
        from app.func import setting
        return setting.record_change(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_normal
def wb_create(request, json_param, user):
    from app.func import wb
    return wb.wb_create(request, json_param, user)

@csrf_exempt
@mywrapper.wrapper_wb
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
@mywrapper.wrapper_wb
def wb_image_get(request, json_param, user, user_wb):
    from app.func import wb
    return wb.wb_image_get(request, json_param, user, user_wb)

@csrf_exempt
@mywrapper.wrapper_wb_file
def wb_image_set(request, user, user_wb):
    checkbit = paramcheck_file(request, 'name', str)
    if type(checkbit) == bool:
        from app.func import wb
        return wb.wb_image_set(request, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_wb
def wb_remove(request, json_param, user, user_wb):
    from app.func import wb
    return wb.wb_remove(request, json_param, user, user_wb)

@csrf_exempt
@mywrapper.wrapper_wb
def wb_type(request, json_param, user, user_wb):
    checkbit = paramcheck(json_param, 'type', int)
    if type(checkbit) == bool:
        from app.func import wb
        return wb.wb_type(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_wb
def word_add(request, json_param, user, user_wb):
    checkbit = paramcheck(json_param, 'word', str)
    if type(checkbit) == bool:
        from app.func import word
        return word.word_add(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_wb
def word_remove(request, json_param, user, user_wb):
    checkbit = paramcheck(json_param, 'word', str)
    if type(checkbit) == bool:
        from app.func import word
        return word.word_remove(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_normal
def friends_namesearch(request, json_param, user):
    checkbit = paramcheck(json_param, 'name', str)
    if type(checkbit) == bool:
        from app.func import friends
        return friends.friends_namesearch(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_normal
def friends_uidsearch(request, json_param, user):
    checkbit = paramcheck(json_param, 'uid', str)
    if type(checkbit) == bool:
        from app.func import friends
        return friends.friends_uidsearch(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)

@csrf_exempt
@mywrapper.wrapper_normal
def friends_list(request, json_param, user):
    from app.func import friends
    return friends.friends_list(request, json_param, user)
      
@csrf_exempt
@mywrapper.wrapper_friends
def friends_follow(request, json_param, user, f_user):
    from app.func import friends
    return friends.friends_follow(request, json_param, user, f_user)

@csrf_exempt
@mywrapper.wrapper_friends
def friends_unfollow(request, json_param, user, f_user):
    from app.func import friends
    return friends.friends_unfollow(request, json_param, user, f_user)
    
@csrf_exempt
@mywrapper.wrapper_friends
def friends_headicon(request, json_param, user, f_user):
    from app.func import friends
    return friends.friends_headicon(request, json_param, user, f_user)
    
@csrf_exempt
@mywrapper.wrapper_friends
def friends_info(request, json_param, user, f_user):
    from app.func import friends
    return friends.friends_info(request, json_param, user, f_user)

@csrf_exempt
@mywrapper.wrapper_friends_wb
def friends_subscribe(request, json_param, user, f_user, f_wb):
    from app.func import friends
    return friends.friends_subscribe(request, json_param, user, f_user, f_wb)
    
@csrf_exempt
@mywrapper.wrapper_friends_wb
def friends_unsubscribe(request, json_param, user, f_user, f_wb):
    from app.func import friends
    return friends.friends_unsubscribe(request, json_param, user, f_user, f_wb)

@csrf_exempt
@mywrapper.wrapper_friends_wb
def friends_wbcover(request, json_param, user, f_user, f_wb):
    from app.func import friends
    return friends.friends_wbcover(request, json_param, user, f_user, f_wb)