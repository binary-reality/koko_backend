from django.http import JsonResponse

def word_add(request, json_param, user, user_wb):
    new_word = json_param['word']
    exist_word = user_wb.wordlist.filter(content=new_word)
    if len(exist_word) == 0:
        user_wb.wordlist.create(list_info=user_wb, content=new_word)
        return JsonResponse({"message": "Word added successfully!"}, status=200)
    elif len(exist_word) == 1:
        return JsonResponse({"message": "Word already exists"}, status=200)
    else:
        return JsonResponse({'message': 'Duplicate word'}, status=401)
    
def word_remove(request, json_param, user, user_wb):
    word = json_param['word']
    exist_word = user_wb.wordlist.filter(content=word)
    if len(exist_word) == 0:
        return JsonResponse({"message": "Word doesn't exist"}, status=404)
    elif len(exist_word) == 1:
        exist_word[0].delete()
        return JsonResponse({"message": "Word removed successfully"}, status=200)
    else:
        for x in exist_word:
            x.delete()
        return JsonResponse({'message': 'Duplicate word'}, status=401)