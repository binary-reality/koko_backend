from django.http import JsonResponse
from app import models
from dicts import dic_func

diction = dic_func.Dic()

def read(request, user):
    from mine import final
    import os
    files = request.FILES
    wavelist = request.POST.get('wave')
    word = request.POST.get('word')
    wave = []
    for x in wavelist:
        if x.isdigit():
            wave.append(int(x))
    openid = request.POST.get('openid')
    audio = files['word.mp3'].read()
    acc_fileName = "./mine/" + openid + "_tmp"
    with open(acc_fileName + ".mp3", "wb") as f:
        f.write(audio)
    result = final.main(acc_fileName + ".mp3", wave)
    os.remove(acc_fileName + ".json")
    os.remove(acc_fileName + ".mp3")
    os.remove(acc_fileName + ".wav")
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
            "message": "Success in word analyzing",
            "accent": result
        },
        status = 200
    )

def search(request, json_param, user):
    word = json_param["searchWord"]
    resultNum = user.reserved_time
    if resultNum > 50:
        resultNum = 50
    return JsonResponse(
        {
            "message": "Success in word searching",
            "results": diction.search_results(word,num=resultNum)
        },
        status = 200
    )

def detail(request, json_param, user):
    word = json_param["word"]
    schrcdlist = user.searchrecord.filter(content=word)
    if len(schrcdlist) == 0:
        models.schrcd.objects.create(owner_openid=user, content=word, schnumber=1)
    elif len(schrcdlist) == 1:
        schrcdlist[0].schnumber = schrcdlist[0].schnumber + 1
        schrcdlist[0].save()
    else:
        return JsonResponse({'message': 'Duplicate records'}, status=401)
    return JsonResponse(
        {
            "message": "Success in word searching",
            "detail": diction.get_detail(word)
        },
        status = 200
    )

def getlist(request, json_param, user):
    word = json_param["type"]
    return JsonResponse(
        {
            "message": "Success in word searching",
            "medicine": diction.medical_list(word)
        },
        status = 200
    )