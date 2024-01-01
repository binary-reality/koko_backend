from django.http import JsonResponse
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

import json
from app import mywrapper
from app.mywrapper import paramcheck, paramcheck_file

# Create your views here.


@csrf_exempt
def hello(request):
    return HttpResponse("Welcome to koko!", status=200)


@csrf_exempt
def login(request):
    """
    @api {post} /login/ login
    @apiName login
    @apiGroup login


    @apiDescription
    此函数用户进行用户登录的检查，从前端发送的请求中获取登录凭证，然后通过微信登录接口得到返回信息。
    会将微信返回的结果返回至前端，并同时附带该用户的大部分信息内容。具体内容见函数详细说明。

    如果登录凭证无效，依然会显示状态码200的返回，但是返回的信息中errcode并非0。

    
    @apiParam {String} code 用户登录凭证
    @apiParamExample {json} 请求样例
        {
            "code": "real_login_code"
        }

        
    @apiSuccess {Dict} user_data 该用户包含的所有数据
    @apiSuccess {String} user_data.file 用户头像文件名称
    @apiSuccess {Dict} user_data.info 用户信息
    @apiSuccess {String} user_data.info.openid 用户openid
    @apiSuccess {String} user_data.info.uid 用户uid
    @apiSuccess {String} user_data.info.nickname 用户昵称
    @apiSuccess {String} user_data.info.timeline 用户搜索记录保存条数
    @apiSuccess {List} user_data.info.followees 用户关注者列表
    @apiSuccess {int} user_data.info.recordOn 是否保存用户读音，0不保存，1保存
    @apiSuccess {int} user_data.info.wbnum 用户单词本数量

    @apiSuccess {List} user_data.flwbs 用户订阅单词本列表
    @apiSuccess {String} user_data.flwbs.name 订阅单词本名称
    @apiSuccess {String} user_data.flwbs.intro 订阅单词本介绍
    @apiSuccess {String} user_data.flwbs.coverUrl 订阅单词本封面名称
    @apiSuccess {Number} user_data.flwbs.id 订阅单词本序号
    @apiSuccess {Number} user_data.flwbs.uid 订阅单词本拥有者uid
    @apiSuccess {Number} user_data.flwbs.following 该单词本是否被本用户订阅
    @apiSuccess {Array} user_data.flwbs.words 单词本中单词

    @apiSuccess {Array} user_data.wordbooks 用户拥有的单词本列表
    @apiSuccess {Number} user_data.wordbooks.id 单词本序号
    @apiSuccess {String} user_data.wordbooks.name 单词本名称
    @apiSuccess {String} user_data.wordbooks.intro 单词本介绍
    @apiSuccess {String} user_data.wordbooks.coverUrl 单词本封面名称
    @apiSuccess {String} user_data.wordbooks.type 单词本类型（公开或私有）
    @apiSuccess {Array} user_data.wordbooks.words 单词本中单词

    @apiSuccess {Array} user_data.wordHistory 搜索记录
    @apiSuccess {String} user_data.wordHistory.content 单词内容
    @apiSuccess {String} user_data.wordHistory.date 最后一次搜索时间
    @apiSuccess {Number} user_data.wordHistory.schnumber 搜索次数

    @apiSuccess {Array} user_data.readHistory 朗读记录
    @apiSuccess {String} user_data.readHistory.content 朗读的单词内容
    @apiSuccess {String} user_data.readHistory.date 最后一次朗读时间
    @apiSuccess {String} user_data.readHistory.lastrd 最后一次朗读具体详情
    @apiSuccess {String} user_data.readHistory.lastres 最后一次朗读是否正确

    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "openid": "user_openid",
            "uid": "user_id",
            "nickname": "user_nickname",
            "timeline": "user_timeline",
            "followees": ["followee1", "followee2"],
            "recordOn": true,
            "wbnum": 3,
            "flwbs": [
                {
                    "name": "wordbook1",
                    "intro": "wordbook1_intro",
                    "coverUrl": "wordbook1_cover_url",
                    "id": 1,
                    "uid": 123,
                    "following": 1,
                    "words": ["word1", "word2"]
                },
                {
                    "name": "wordbook2",
                    "intro": "wordbook2_intro",
                    "coverUrl": "wordbook2_cover_url",
                    "id": 2,
                    "uid": 456,
                    "following": 0,
                    "words": ["word3", "word4"]
                }
            ],
            "wordbooks": [
                {
                    "id": 1,
                    "name": "wordbook3",
                    "intro": "wordbook3_intro",
                    "coverUrl": "wordbook3_cover_url",
                    "type": "public",
                    "words": ["word5", "word6"]
                },
                {
                    "id": 2,
                    "name": "wordbook4",
                    "intro": "wordbook4_intro",
                    "coverUrl": "wordbook4_cover_url",
                    "type": "private",
                    "words": ["word7", "word8"]
                }
            ],
            "wordHistory": [
                {
                    "content": "word9",
                    "date": "2023-01-01",
                    "schnumber": 123
                },
                {
                    "content": "word10",
                    "date": "2023-01-02",
                    "schnumber": 456
                }
            ],
            "readHistory": [
                {
                    "content": "word11",
                    "date": "2023-01-03",
                    "lastrd": "2023-01-02",
                    "lastres": "pass"
                },
                {
                    "content": "word12",
                    "date": "2023-01-04",
                    "lastrd": "2023-01-03",
                    "lastres": "fail"
                }
            ]
        }

    
    @apiError {String} message 错误信息
    @apiErrorExample {json} 请求方式错误
        HTTP/1.1 405 Method Not Allowed
        {
            "message": "Method not allowed"
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
    if request.method == "POST":
        json_param = json.loads(request.body)
        checkbit = paramcheck(json_param, 'code', str)
        if isinstance(checkbit, bool):
            from app.func import login
            return login.login(request, json_param)
        else:
            return JsonResponse({'message': checkbit}, status=400)
    else:
        return JsonResponse({"message": "Method not allowed"}, status=405)


@csrf_exempt
@mywrapper.wrapper_normal
def getlogheadicon(request, json_param, user):
    """
    @api {post} /login/headicon/ getlogheadicon
    @apiName getlogheadicon
    @apiGroup login

    
    @apiDescription
    此函数用于获取用户头像。


    @apiParam {String} openid 用户openid
    @apiParamExample {json} 请求样例
        {
            "openid": "user_openid"
        }

        
    @apiSuccess {File} image 用户头像文件内容
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        File (headicon.jpg)
    
        
    @apiUse wrapper_normal_error
    """
    from app.func import login
    return login.getlogheadicon(request, json_param, user)


@csrf_exempt
@mywrapper.wrapper_file
def read(request, user):
    """
    @api {post} /read/ read
    @apiName read
    @apiGroup read


    @apiDescription
    此函数用于进行发音分析与结果返回。

    发音分析的结果为数组，如[0,1,1]，其中0表示相对低音，1表示相对高音。


    @apiParam {File} word.mp3 用户的朗读音频文件
    @apiParam {String} wave 用户朗读的单词的正确的读音
    @apiParam {String} word 用户朗读的单词
    @apiParam {String} openid 发出请求的用户openid


    @apiSuccess {String} message 成功信息
    @apiSuccess {String} accent 用户读音分析结果
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Success in word analyzing",
            "accent": "[0,1,1]"
        }

        
    @apiUse wrapper_normal_error
    """
    checkbit = paramcheck_file(request, 'wave', str)
    if not isinstance(checkbit, bool):
        return JsonResponse({'message': checkbit}, status=400)
    checkbit = paramcheck_file(request, 'word', str)
    if not isinstance(checkbit, bool):
        return JsonResponse({'message': checkbit}, status=400)
    from app.func import read
    return read.read(request, user)


@csrf_exempt
@mywrapper.wrapper_normal
def search(request, json_param, user):
    """
    @api {post} /search/ search
    @apiName search
    @apiGroup read

    
    @apiDescription
    此函数用于根据提供的内容进行单词搜索。

    搜索条目数上限最大50条。


    @apiParam {String} searchWord 带搜索的单词
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "searchWord": "word",
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccess {Array} results 搜索到的单词列表
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Success in word searching",
            "results": [
                "word1",
                "word2",
                ...
            ]
        }


    @apiUse wrapper_normal_error
    """
    checkbit = paramcheck(json_param, 'searchWord', str)
    if isinstance(checkbit, bool):
        from app.func import read
        return read.search(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_normal
def detail(request, json_param, user):
    """
    @api {post} /detail/ detail
    @apiName detail
    @apiGroup read

    
    @apiDescription
    此函数用于获得搜索单词的详情，包括读音、解释与例句等。


    @apiParam {String} word 需要获得详情的单词
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "word": "word",
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccess {Object} detail 单词详情
    @apiSuccessExample {json} 成功返回样例
        HTTP/1.1 200 OK
        {
            "message": "Success in word searching",
            "detail": {
                "赤い【あかい◎】":{
                    "name":"赤い【あかい◎】"           //本体名字
                    "accent":0,                       //未标声调时用-1
                    "kana":["あ","か","い"],           //单拍平假名列表
                    "taka":[0,1,1]                     //真实假名高低，不显示促音
                    "wave":[0,1,1],                   //每拍假名的高低,2表示促音
                    "type":"形",                       //词性,可能为空
                    "exsent":[                         //解释及例句的词典的列表，可能为空
                        {
                            "explan":"红色的",           //解释
                            "sentJap":["時が虚しく過ぎる。"],               //例句日文列表，可能为空
                            "sentChi":["虚度时光。"]                //例句中文列表
                        },
                        {
                            ……
                        }
                    ]
                }
            }
        }

        
    @apiUse wrapper_normal_error
    @apiErrorExample {json} 搜索到重复单词
        HTTP/1.1 403 Forbidden
        {
            "message": "User Duplicate records"
        }
    """
    checkbit = paramcheck(json_param, 'word', str)
    if isinstance(checkbit, bool):
        from app.func import read
        return read.detail(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_normal
def getlist(request, json_param, user):
    """
    @api {post} /list/ getlist
    @apiName getlist
    @apiGroup read

    
    @apiDescription
    此函数用于获取训练列表，根据前端请求的音型返回列表。


    @apiParam {Number} type 单词的音型
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "type": 2,
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccess {Array} medicine 返回的单词列表
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Success in word searching",
            "medicine": [
                "word1":{
                    ...
                },
                "word2":{
                    ...
                },
                ...
            ]
        }
    
        
    @apiUse wrapper_normal_error
    """
    checkbit = paramcheck(json_param, 'type', int)
    if isinstance(checkbit, bool):
        from app.func import read
        return read.getlist(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_file
def headicon_change(request, user):
    """
    @api {post} /setting/headIcon/ headicon_change
    @apiName headicon_change
    @apiGroup setting


    @apiDescription
    此函数用户更改用户头像。


    @apiParam {File} headIcon 新的用户头像文件
    @apiParam {String} name 新用户头像文件名
    @apiParam {String} openid 发起请求的用户openid


    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功请求样例
        HTTP/1.1 200 OK
        {
            "message": "Headicon successfully changed"
        }
    
        
    @apiUse wrapper_normal_error
    """
    checkbit = paramcheck_file(request, 'name', str)
    if isinstance(checkbit, bool):
        from app.func import setting
        return setting.headicon_change(request, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_normal
def nickname_change(request, json_param, user):
    """
    @api {post} /setting/nickname/ nickname_change
    @apiName nickname_change
    @apiGroup setting


    @apiDescription
    此函数用于更改用户昵称。


    @apiParam {String} nickname 新昵称
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "nickname": "new_nickname",
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Nickname successfully changed"
        }

        
    @apiUse wrapper_normal_error
    """
    checkbit = paramcheck(json_param, 'nickname', str)
    if isinstance(checkbit, bool):
        from app.func import setting
        return setting.nickname_change(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_normal
def timeline_change(request, json_param, user):
    """
    @api {post} /setting/timeline/ timeline_change
    @apiName timeline_change
    @apiGroup setting


    @apiDescription
    此函数用于更改单词搜索保留词条数。

    
    @apiParam {Number} timeline 新的单词搜索保留词条数
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "timeline": "new_timeline",
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Timeline successfully changed"
        }
    
        
    @apiUse wrapper_normal_error
    """
    checkbit = paramcheck(json_param, 'timeline', int)
    if isinstance(checkbit, bool):
        from app.func import setting
        return setting.timeline_change(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_normal
def record_change(request, json_param, user):
    """
    @api {post} /setting/record/ record_change
    @apiName record_change
    @apiGroup setting


    @apiDescription
    此函数用于更改录音是否保留的配置。


    @apiParam {String} recordOn 用户是否保存录音的新属性
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "recordOn": "False",
            "openid": "user_openid"
        }

    
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Record button successfully changed"
        }


    @apiUse wrapper_normal_error
    @apiErrorExample {json} 发送的请求中参数内容无法识别
        HTTP/1.1 400 Bad Request
        {
            "message": "Invalid request argument: recordOn"
        }
    
    """
    checkbit = paramcheck(json_param, 'recordOn', str)
    if isinstance(checkbit, bool):
        from app.func import setting
        return setting.record_change(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_normal
def wb_create(request, json_param, user):
    """
    @api {post} /wb/create/ wb_create
    @apiName wb_create
    @apiGroup wb


    @apiDescription
    此函数用于创建单词本。


    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "New wordbook successfully created"
        }

        
    @apiUse wrapper_normal_error
    """
    from app.func import wb
    return wb.wb_create(request, json_param, user)


@csrf_exempt
@mywrapper.wrapper_wb
def wb_info_change(request, json_param, user, user_wb):
    """
    @api {post} /wb/info/ wb_info_change
    @apiName wb_info_change
    @apiGroup wb


    @apiDescription
    此函数用于更改单词本信息，不包括单词本封面。


    @apiParam {String} name 单词本的新名称
    @apiParam {String} intro 单词本的新介绍
    @apiParam {Number} index 单词本的序号   
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "name": "new_name",
            "intro": "new_intro",
            "index": 1,
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Wordbook information successfully changed"
        }

        
    @apiUse wrapper_wb_error
    """
    checkbit = paramcheck(json_param, 'name', str)
    if not isinstance(checkbit, bool):
        return JsonResponse({'message': checkbit}, status=400)
    checkbit = paramcheck(json_param, 'intro', str)
    if isinstance(checkbit, bool):
        from app.func import wb
        return wb.wb_info_change(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_wb
def wb_image_get(request, json_param, user, user_wb):
    """
    @api {post} /wb/image/get/ wb_image_get
    @apiName wb_image_get
    @apiGroup wb


    @apiDescription
    此函数用于获得单词本封面图像。


    @apiParam {Number} index 单词本的序号   
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "index": 1,
            "openid": "user_openid"
        }

        
    @apiSuccess {File} image 单词本封面内容
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        File (wordbook_cover.jpg)

    
    @apiUse wrapper_wb_error
    """
    from app.func import wb
    return wb.wb_image_get(request, json_param, user, user_wb)


@csrf_exempt
@mywrapper.wrapper_wb_file
def wb_image_set(request, user, user_wb):
    """
    @api {post} /wb/image/set/ wb_image_set
    @apiName wb_image_set
    @apiGroup wb


    @apiDescription
    此函数用于更改单词本封面图像。


    @apiParam {String} name 新单词本封面名称
    @apiParam {File} image 新单词本封面内容
    @apiParam {Number} index 单词本的序号   
    @apiParam {String} openid 发起请求的用户openid


    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Wordbook image successfully changed!"
        }

        
    @apiUse wrapper_wb_error
    """
    checkbit = paramcheck_file(request, 'name', str)
    if isinstance(checkbit, bool):
        from app.func import wb
        return wb.wb_image_set(request, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_wb
def wb_remove(request, json_param, user, user_wb):
    """
    @api {post} /wb/remove/ wb_remove
    @apiName wb_remove
    @apiGroup wb


    @apiDescription
    此函数用于删除单词本。

    在删除一个单词本之后，所有序号大于被删除单词本的单词本序号均会前移。

    
    @apiParam {Number} index 单词本的序号   
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "index": 1,
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Wordbook removed successfully"
        }

        
    @apiUse wrapper_wb_error
    """
    from app.func import wb
    return wb.wb_remove(request, json_param, user, user_wb)


@csrf_exempt
@mywrapper.wrapper_wb
def wb_type(request, json_param, user, user_wb):
    """
    @api {post} /wb/type/ wb_type
    @apiName wb_type
    @apiGroup wb


    @apiDescription
    此函数用于更改单词本类型。

    
    @apiParam {String} type 新单词本类型，0公开1私有
    @apiParam {Number} index 单词本的序号   
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "index": 1,
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Wordbook privacy successfully changed"
        }


    @apiUse wrapper_wb_error
    """
    checkbit = paramcheck(json_param, 'type', int)
    if isinstance(checkbit, bool):
        from app.func import wb
        return wb.wb_type(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_wb
def word_add(request, json_param, user, user_wb):
    """
    @api {post} /word/add/ word_add
    @apiName word_add
    @apiGroup word


    @apiDescription
    此函数用于向单词本中增加单词。


    @apiParam {String} word 需要增加的新单词
    @apiParam {Number} index 单词本序号
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "word": "new_word",
            "index": 1,
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Word added successfully!"
        }
    
        
    @apiUse wrapper_wb_error
    @apiErrorExample {json} 单词已经被添加
        HTTP/1.1 403 Forbidden
        {
            "message": "Word already exists"
        }
    @apiErrorExample {json} 搜索到单词本中存在重复单词
        HTTP/1.1 403 Forbidden
        {
            "message": "Duplicate word"
        }
    """
    checkbit = paramcheck(json_param, 'word', str)
    if isinstance(checkbit, bool):
        from app.func import word
        return word.word_add(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_wb
def word_remove(request, json_param, user, user_wb):
    """
    @api {post} /word/remove/ word_remove
    @apiName word_remove
    @apiGroup word


    @apiDescription
    此函数用于将单词从单词本中移除。


    @apiParam {String} word 需要移除的单词
    @apiParam {Number} index 单词本序号
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "word": "word",
            "index": 1,
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Word removed successfully"
        }
    
        
    @apiUse wrapper_wb_error
    @apiErrorExample {json} 单词本中该单词不存在
        HTTP/1.1 404 Not Found
        {
            "message": "Word doesn't exist"
        }
    @apiErrorExample {json} 单词本中出现重复单词
        HTTP/1.1 403 Forbidden
        {
            "message": "Duplicate word"
        }
    """
    checkbit = paramcheck(json_param, 'word', str)
    if isinstance(checkbit, bool):
        from app.func import word
        return word.word_remove(request, json_param, user, user_wb)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_normal
def friends_namesearch(request, json_param, user):
    """
    @api {post} /friends/namesearch/ friends_namesearch
    @apiName friends_namesearch
    @apiGroup friends


    @apiDescription
    此函数用于通过昵称来搜索用户。

    只有昵称完全相同的用户才可以被搜索到。

    
    @apiParam {String} name 待搜索的用户昵称
    @apiParam {String} openid 发起搜索的用户自己的openid
    @apiParamExample {json} 请求样例
        {
            "name": "friend_name",
            "openid": "user_openid"
        }

        
    @apiSuccess {Array} result 返回的所有昵称符合的用户信息列表，每一项内容依次为uid，昵称，头像名，是否关注该用户
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "result": [
                [123, "friend1", "headicon_url1", 1],
                [456, "friend2", "headicon_url2", 0]
            ]
        }

        
    @apiUse wrapper_normal_error
    @apiErrorExample {json} 未找到昵称匹配的用户
        HTTP/1.1 404 Not Found
        {
            "message": "User not found"
        }
    """
    checkbit = paramcheck(json_param, 'name', str)
    if isinstance(checkbit, bool):
        from app.func import friends
        return friends.friends_namesearch(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_normal
def friends_uidsearch(request, json_param, user):
    """
    @api {post} /friends/uidsearch/ friends_uidsearch
    @apiName friends_uidsearch
    @apiGroup friends


    @apiDescription
    此函数用于通过uid搜索用户。

    只有uid完全相同的用户才能被搜索到。


    @apiParam {String} uid 带搜索的用户uid
    @apiParam {String} openid 发起搜索的用户openid
    @apiParamExample {json} 请求样例
        {
            "uid": "uid",
            "openid": "user_openid"
        }

        
    @apiSuccess {Array} result 返回的用户列表，每一项内容依次为uid，昵称，头像名，是否关注该用户
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "result": [
                [123, "friend1", "headicon_url1", 1]
            ]
        }

        
    @apiUse wrapper_normal_error
    @apiErrorExample {json} 未找到uid匹配的用户
        HTTP/1.1 404 Not Found
        {
            "message": "User not found"
        }
    @apiErrorExample {json} 出现uid重复用户
        HTTP/1.1 403 Forbidden
        {
            "message": "Duplicate users"
        }
    """
    checkbit = paramcheck(json_param, 'uid', str)
    if isinstance(checkbit, bool):
        from app.func import friends
        return friends.friends_uidsearch(request, json_param, user)
    else:
        return JsonResponse({'message': checkbit}, status=400)


@csrf_exempt
@mywrapper.wrapper_normal
def friends_list(request, json_param, user):
    """
    @api {post} /friends/list/ friends_list
    @apiName friends_list
    @apiGroup friends


    @apiDescription
    此函数用于获取用户的关注列表。


    @apiParam {String} openid 请求列表用户的openid
    @apiParamExample {json} 请求样例
        {
            "openid": "user_openid"
        }
    
        
    @apiSuccess {Array} result 返回该用户的所有关注列表，每一项内容依次为uid，昵称，头像名，是否关注该用户
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "result": [
                [123, "friend1", "headicon_url1"],
                [456, "friend2", "headicon_url2"]
            ]
        }


    @apiUse wrapper_normal_error
    """
    from app.func import friends
    return friends.friends_list(request, json_param, user)


@csrf_exempt
@mywrapper.wrapper_friends
def friends_follow(request, json_param, user, f_user):
    """
    @api {post} /friends/follow/ friends_follow
    @apiName friends_follow
    @apiGroup friends


    @apiDescription
    此函数用于关注其他用户。


    @apiParam {Number} uid 需要关注的用户uid
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "uid": 123,
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功消息
    @apiSuccessExample {json} 成功返回样例
        HTTP/1.1 200 OK
        {
            "message": "Successfully followed"
        }

        
    @apiUse wrapper_friends_error
    @apiErrorExample {json} 目标用户已经关注
        HTTP/1.1 403 Forbidden
        {
            "message": "Already followed"
        }
    """
    from app.func import friends
    return friends.friends_follow(request, json_param, user, f_user)


@csrf_exempt
@mywrapper.wrapper_friends
def friends_unfollow(request, json_param, user, f_user):
    """
    @api {post} /friends/unfollow/ friends_unfollow
    @apiName friends_unfollow
    @apiGroup friends


    @apiDescription
    此函数用于对其他用户进行取消关注。


    @apiParam {Number} uid 需要取消关注的用户uid
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "uid": 123,
            "openid": "user_openid"
        }


    @apiSuccess {String} message 成功消息
    @apiSuccessExample {json} 成功响应请求
        HTTP/1.1 200 OK
        {
            "message": "Successfully unfollowed"
        }

        
    @apiUse wrapper_friends_error
    @apiErrorExample {json} 需要取消关注的用户未关注
        HTTP/1.1 403 Forbidden
        {
            "message": "Not followed"
        }
    """
    from app.func import friends
    return friends.friends_unfollow(request, json_param, user, f_user)


@csrf_exempt
@mywrapper.wrapper_friends
def friends_headicon(request, json_param, user, f_user):
    """
    @api {post} /friends/headicon/ friends_headicon
    @apiName friends_headicon
    @apiGroup friends


    @apiDescription
    此函数用于获得其他用户的头像。


    @apiParam {Number} uid 需要获得头像的用户uid
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "uid": 123,
            "openid": "user_openid"
        }

        
    @apiSuccess {File} image 用户头像
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        File (headicon.jpg)


    @apiUse wrapper_friends_error
    """
    from app.func import friends
    return friends.friends_headicon(request, json_param, user, f_user)


@csrf_exempt
@mywrapper.wrapper_friends
def friends_info(request, json_param, user, f_user):
    """
    @api {post} /friends/info/ friends_info
    @apiName friends_info
    @apiGroup friends


    @apiDescription
    此函数用于获得其他用户的部分信息。


    @apiParam {Number} uid 需要获得内容的用户uid
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "uid": 123,
            "openid": "user_openid"
        }

        
    @apiSuccess {Dict} detail 请求需要获得的用户内容全体
    @apiSuccess {Dict} detail.info 用户的信息
    @apiSuccess {String} detail.info.nickname 用户的昵称
    @apiSuccess {Number} detail.info.following 是否关注了该用户

    @apiSuccess {Array} detail.wordbooks 该用户拥有的单词本
    @apiSuccess {Number} detail.wordbooks.id 单词本的序号
    @apiSuccess {Number} detail.wordbooks.uid 该单词本所属的用户uid
    @apiSuccess {String} detail.wordbooks.name 单词本名称
    @apiSuccess {String} detail.wordbooks.intro 单词本介绍
    @apiSuccess {String} detail.wordbooks.coverUrl 单词本封面名称
    @apiSuccess {Number} detail.wordbooks.type 单词本类型（共有或私有）
    @apiSuccess {Number} detail.wordbooks.following 发起请求的用户是否订阅了该单词本
    @apiSuccess {Array} detail.wordbooks.words 单词本中的单词

    @apiSuccess {Array} detail.readHistory 用户朗读记录
    @apiSuccess {String} detail.readHistory.content 单词内容
    @apiSuccess {String} detail.readHistory.date 最后一次朗读时间
    @apiSuccess {String} detail.readHistory.lastrd 最后一次朗读记录内容
    @apiSuccess {String} detail.readHistory.lastres 最后一次朗读结果

    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "detail": {
                "info": {
                    "nickname": "friend1",
                    "following": 1
                },
                "wordbooks": [
                    {
                        "id": 1,
                        "uid": 123,
                        "name": "wordbook1",
                        "intro": "wordbook1_intro",
                        "coverUrl": "wordbook1_cover_url",
                        "type": "public",
                        "following": 1,
                        "words": ["word1", "word2"]
                    },
                    {
                        "id": 2,
                        "uid": 123,
                        "name": "wordbook2",
                        "intro": "wordbook2_intro",
                        "coverUrl": "wordbook2_cover_url",
                        "type": "private",
                        "following": 0,
                        "words": ["word3", "word4"]
                    }
                ],
                "readHistory": [
                    {
                        "content": "word5",
                        "date": "2023-01-01",
                        "lastrd": "2023-01-02",
                        "lastres": "pass"
                    },
                    {
                        "content": "word6",
                        "date": "2023-01-03",
                        "lastrd": "2023-01-04",
                        "lastres": "fail"
                    }
                ]
            }
        }


    @apiUse wrapper_friends_error
    """
    from app.func import friends
    return friends.friends_info(request, json_param, user, f_user)


@csrf_exempt
@mywrapper.wrapper_friends_wb
def friends_subscribe(request, json_param, user, f_user, f_wb):
    """
    @api {post} /friends/subscribe/ friends_subscribe
    @apiName friends_subscribe
    @apiGroup friends


    @apiDescription
    此函数用于订阅单词本。


    @apiParam {Number} uid 所订阅的单词本所属的用户的uid
    @apiParam {Number} id 所订阅的单词本的序号
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "uid": 123,
            "id": 1,
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Successfully subscribed"
        }

        
    @apiUse wrapper_friends_wb_error
    @apiErrorExample {json} 需要订阅的单词本已经订阅
        HTTP/1.1 403 Forbidden
        {
            "message": "Already followed"
        }
    @apiErrorExample {json} 出现重复订阅单词本
        HTTP/1.1 403 Forbidden
        {
            "message": "Duplicate wordbooks"
        }
    """
    from app.func import friends
    return friends.friends_subscribe(request, json_param, user, f_user, f_wb)


@csrf_exempt
@mywrapper.wrapper_friends_wb
def friends_unsubscribe(request, json_param, user, f_user, f_wb):
    """
    @api {post} /friends/unsubscribe/ friends_unsubscribe
    @apiName friends_unsubscribe
    @apiGroup friends


    @apiDescription
    此函数用于取消订阅单词本。


    @apiParam {Number} uid 所订阅的单词本所属的用户的uid
    @apiParam {Number} id 所订阅的单词本的序号
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "uid": 123,
            "id": 1,
            "openid": "user_openid"
        }

        
    @apiSuccess {String} message 成功信息
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        {
            "message": "Successfully unsubscribed"
        }

        
    @apiUse wrapper_friends_wb_error
    @apiErrorExample {json} 需要取消订阅的单词本未订阅
        HTTP/1.1 403 Forbidden
        {
            "message": "Wordbook not subscribed"
        }
    @apiErrorExample {json} 出现重复订阅单词本
        HTTP/1.1 403 Forbidden
        {
            "message": "Duplicate wordbooks"
        }
    """
    from app.func import friends
    return friends.friends_unsubscribe(request, json_param, user, f_user, f_wb)


@csrf_exempt
@mywrapper.wrapper_friends_wb
def friends_wbcover(request, json_param, user, f_user, f_wb):
    """
    @api {post} /friends/wbcover/ friends_wbcover
    @apiName friends_wbcover
    @apiGroup friends


    @apiDescription
    此函数用户获取其他用户的单词本封面。


    @apiParam {Number} uid 其他用户单词本所属的用户的uid
    @apiParam {Number} id 其他用户单词本的序号
    @apiParam {String} openid 发起请求的用户openid
    @apiParamExample {json} 请求样例
        {
            "uid": 123,
            "id": 1,
            "openid": "user_openid"
        }

        
    @apiSuccess {File} image 其他用户单词本的封面内容
    @apiSuccessExample {json} 成功响应样例
        HTTP/1.1 200 OK
        File (wordbook_cover.jpg)


    @apiUse wrapper_friends_wb_error
    """
    from app.func import friends
    return friends.friends_wbcover(request, json_param, user, f_user, f_wb)
