from django.http import JsonResponse
from django.http import FileResponse

def wb_create(request, json_param, user):
    cur_wbnumber = user.wdlistnumber
    user.wbinfo.create(owner_openid=user, index=cur_wbnumber+1, name="未命名单词本"+str(cur_wbnumber+1), intro="这是单词本的介绍")
    user.wdlistnumber = user.wdlistnumber + 1
    user.save()
    return JsonResponse({"message": "New wordbook successfully created"}, status=200)

def wb_info_change(request, json_param, user, user_wb):
    user_wb.name = json_param['name']
    user_wb.intro = json_param['intro']
    user_wb.save()
    return JsonResponse({"message": "Wordbook information successfully changed"}, status=200)

def wb_image_get(request, json_param, user, user_wb):
    return FileResponse(user_wb.image, as_attachment=True, filename=user_wb.image_name, status=200)

def wb_image_set(request, user, user_wb):
    import os
    from koko import settings
    name = request.POST.get('name')
    openid = request.POST.get('openid')
    wbindex = request.POST.get('index')
    name_list = name.split(".")
    new_image = request.FILES.get("image")
    image_name = "wb" + str(wbindex) + "_" + openid + "." + name_list[1]
    if user_wb.image_name != "../../images/dictimage/dictimage3.png":
        os.remove(os.path.join(settings.MEDIA_ROOT, user_wb.image.name))
    user_wb.image_name = image_name
    user_wb.image = new_image
    user_wb.save()
    return JsonResponse({"message": "Wordbook image successfully changed!"}, status=200)

def wb_remove(request, json_param, user, user_wb):
    user_wb.delete()
    wbindex = json_param['index']
    for i in range(wbindex + 1, user.wdlistnumber + 1):
        rev_wb = user.wbinfo.get(index=i)
        rev_wb.index = rev_wb.index - 1
        rev_wb.save()
    user.wdlistnumber = user.wdlistnumber - 1
    user.save()
    return JsonResponse({"message": "Wordbook removed successfully"}, status=200)

def wb_type(request, json_param, user, user_wb):
    privacy = json_param['type']
    user_wb.public_ctrl = privacy
    user_wb.save()
    return JsonResponse({"message": "Wordbook privacy successfully changed"}, status=200)