from readmdict import MDX
import json
import re
'''
请勿随意运行本文件，可能损坏词典！
本文件目的为生成词典存储格式json
键值对例如
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
'''


circled_numbers_dict = {
    "◎": 0,
    "①": 1,
    "②": 2,
    "③": 3,
    "④": 4,
    "⑤": 5,
    "⑥": 6,
    "⑦": 7,
    "⑧": 8
}

small_kana = [
    "ぁ", "ァ", "ぃ", "ィ", "ぅ", "ゥ", "ぇ", "ェ", "ぉ", "ォ",
    "ㇱ", "ㇲ", "ㇳ", "ㇵ", "ㇶ", "ㇷ", "ㇷ゚", "ㇸ", "ㇹ", "ㇺ", "ㇻ", "ㇼ", "ㇽ", "ㇾ", "ㇿ", "ㇰ", "ㇴ",
    "ゃ", "ャ", "ゅ", "ュ", "ょ", "ョ",
    "ゎ", "ヮ"
]


def get_feature(word):
    '''
    获取形如"赤い【あかい◎】"格式字符串中的属性
    '''
    results = {}
    results["name"] = word
    start = word.find("【") + 1
    end = len(word) - 1

    if word[-2] in circled_numbers_dict.keys():
        accent = circled_numbers_dict[word[-2]]
        end -= 1
        seq = -3
        while word[seq] in circled_numbers_dict.keys():
            accent = circled_numbers_dict[word[seq]]
            end -= 1
            seq -= 1
    else:
        accent = -1
    results["accent"] = accent
    sub = word[start:end]
    kanas = []
    kanas.append(sub[0])
    for c in sub[1:]:
        if c in small_kana:
            kanas[-1] += c
        else:
            kanas.append(c)
    results["kana"] = kanas
    if accent <= 0:
        wave = [1] * len(kanas)
        wave[0] = 0
    elif accent == 1:
        wave = [0] * len(kanas)
        wave[0] = 1
    else:
        wave = [0] * len(kanas)
        for i in range(1, min(accent, len(kanas))):
            wave[i] = 1
    results["taka"] = wave.copy()
    for i, c in enumerate(kanas):
        if c == 'っ':
            wave[i] = 2
    results["wave"] = wave
    return results


def get_expl(html):
    results = {}
    exsent = []
    cxp = r'cixing_title">(.*?)</div'
    type = re.search(cxp, html)
    if type:
        results["type"] = type.groups()[0]
    else:
        results["type"] = "合成词（大概）"

    res = r'explanation">(.*?)<(?:/div><div class="sentence"><div class="sentence_o">(.*?)<.*?sentence_t">(.*?)</div><)*'
    senjap = r'sentence_o">(.*?)<'
    senchi = r'sentence_t">(.*?)<'
    result = re.finditer(res, html)
    for match in result:
        one_exs = {}
        one_exs["explan"] = match.groups()[0]
        one_exs["sentJap"] = re.findall(senjap, match.group())
        one_exs["sentChi"] = re.findall(senchi, match.group())
        exsent.append(one_exs)
    results["exsent"] = exsent
    return results


def filter_and_save_mdx(input_mdx_file, output_file):
    # 打开原始MDX文件和新MDX文件
    input_mdx = MDX(input_mdx_file, encoding='utf-8')
    output_mdx = {}
    items = input_mdx.items()
    # 遍历原始MDX文件中的键值对
    for key, value in items:
        word = key.decode().strip()
        # 如果键在keys_to_keep中，将键值对写入新MDX文件
        if '【' in word:  # and len(word) % 2 == 1:
            output_mdx[word] = get_feature(word)
            output_mdx[word].update(get_expl(value.decode()))

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(output_mdx, f, indent=4, ensure_ascii=False)


# 原始MDX文件和新MDX文件的文件路径
input_mdx_file = "dics/moji.mdx"
output_mdx_file = "dics/koko.json"

# filter_and_save_mdx(input_mdx_file, output_mdx_file)


def search_word(query_word, mdx_file=input_mdx_file):
    # 从mdx查询
    mdx_file = "./dics/moji.mdx"
    mdx = MDX(mdx_file, encoding='utf-8')
    items = mdx.items()
    results = {}
    for key, value in items:
        word = key.decode().strip()
        if query_word in word:
            print(word, "-----", value.decode())
            get_expl(value.decode())
            results[word] = key
    return results


def search_results(query_word):
    # 从json文件查询
    f = open("dics/koko.json", 'r', encoding="utf-8")
    content = f.read()
    dic = json.loads(content)
    items = dic.items()
    results = []
    for word, value in items:
        if query_word in word:
            print(word, "-----", value)
            results.append(word)
    return results


# 查词，返回单词和html文件
queryWord = 'あかい'
search_word(queryWord)
print(search_results(queryWord))
