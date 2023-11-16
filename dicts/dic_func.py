import json
import random

class Dic():
    '''
    字典类
    只要创建一个示例，然后调用函数就行
    funcs:
        search_results
        get_detail
        medical_list
    '''
    def __init__(self) -> None:
        f=open("dicts/koko.json",'r',encoding="utf-8")
        content=f.read()
        self.d=json.loads(content)
        self.items=self.d.items()

    def search_results(self,query_word):
        '''
        param:query_word=搜索内容
        return:字符串列表，形如['赤い【あかい◎】', ……]元素就是字典中的key
        '''
        results=[]
        for word in self.d.keys():
            if query_word in word:
                results.append(word)
        return results[:20]
    
    def get_detail(self,word):
        '''
        param:word='赤い【あかい◎】',字典中的key
        return:字典，包括该单词各种信息。
        '''
        return self.d[word]
    
    def medical_list(self,type):
        '''
        param:type=k，为0-10之间的数字，对应0型音到8型音、促音、长音
        return:字典列表，包含最多十个对应类型的单词详情字典
        '''
        typelist = [
            "◎",
            "①",
            "②",
            "③",
            "④",
            "⑤",
            "⑥",
            "⑦",
            "⑧",
            "っ",
            "ー"
        ]
        results = []
        for word in self.d.keys():
            if typelist[type] in word and self.d[word]["accent"] != -1:
                results.append(self.d[word])
        return random.sample(results,10)
    


# 测试部分
# dict=Dic()
# sr = dict.search_results("⑧")
# print(sr)
# print(dict.get_detail(sr[0]))
# print(dict.medical_list(9))