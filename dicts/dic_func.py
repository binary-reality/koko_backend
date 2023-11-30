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
        f=open("dics/koko.json",'r',encoding="utf-8")
        content=f.read()
        self.d=json.loads(content)
        self.items=self.d.items()

    def search_results(self,query_word):
        '''
        param:query_word=搜索内容
        return:字符串列表，形如['赤い【あかい◎】', ……]元素就是字典中的key
        '''
        first=[]
        for word in self.d.keys():
            if query_word in word:
                first.append(word)
        results=[]
        newl=first[:]
        for word in newl:
            if query_word == word[0:len(query_word)]:
                results.append(word)
                first.remove(word)
        kanaWord="【"+query_word
        newl=first[:]
        for word in newl:
            if kanaWord in word:
                results.append(word)
                first.remove(word)
        for word in first:
            if query_word in word:
                results.append(word)
        return results
    
    def get_detail(self,word):
        '''
        param:word='赤い【あかい◎】',字典中的key
        return:字典，包括该单词各种信息。
        '''
        if word in self.d.keys():
            return self.d[word]
        else:
            return {}
    
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
import time


t = time.time()
dict=Dic()
for e in dict.search_results("そら"):
    print(e)
# print(f'coast:{time.time() - t:.4f}s')

# sr = dict.search_results("③◎")
# print(f'coast:{time.time() - t:.4f}s')
# print(sr)
# print(dict.get_detail(sr[0]))
# print(dict.medical_list(9))
# sr = dict.search_results("そら")
# print(f'coast:{time.time() - t:.4f}s')
# print("--------------------------------")
# print(" ")
# sr = dict.search_results("こお")
# print(f'coast:{time.time() - t:.4f}s')
# print("--------------------------------")
# print(" ")
# sr = dict.search_results("げ")
# print(f'coast:{time.time() - t:.4f}s')
# print("--------------------------------")
# print(" ")
# sr = dict.search_results("おおお")
# print(f'coast:{time.time() - t:.4f}s')
# print("--------------------------------")
# print(" ")
# sr = dict.search_results("ぴん")
# print(f'coast:{time.time() - t:.4f}s')
