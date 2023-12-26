from django.http import JsonResponse

def headicon_change(request, json_param, user):
    import os
    from koko import settings
    files = request.FILES
    image = files.get("headIcon")
    name = json_param['name']
    image_url_list = name.split('.')
    openid = json_param['openid']
    image_name = openid + "." + image_url_list[1]
    if user.headicon_name != 'headicon.png':
        os.remove(os.path.join(settings.MEDIA_ROOT, user.headicon.name))
    user.headicon_name = image_name
    user.headicon = image
    user.save()
    return JsonResponse({"message": "Headicon successfully changed"}, status=200)


def nickname_change(request, json_param, user):
    new_nickname = json_param['nickname']
    user.nickname = new_nickname
    user.save()
    return JsonResponse({"message": "Nickname successfully changed"}, status=200)

def timeline_change(request, json_param, user):
    new_timeline = json_param["timeline"]
    user.reserved_time = new_timeline
    user.save()
    return JsonResponse({"message": "Timeline successfully changed"}, status=200)

def record_change(request, json_param, user):
    new_record = json_param["recordOn"]
    if new_record == "False" or new_record == "false" or new_record == "0":
        user.read_keep = 0
    elif new_record == "True" or new_record == "true" or new_record == "1":
        user.read_keep = 1
    else:
        return JsonResponse({"message": "Invalid request argument: recordOn"}, status=400)
    user.save()
    return JsonResponse({"message": "Record button successfully changed"}, status=200)