from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json

class LoginAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')  

    def test_login_with_valid_credentials(self):
        """
        测试有效凭证的登录。
        """
        response = self.client.post(self.login_url, {'code': '3e5428-ff58yj5'}, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNotNone(response_data.get('openid'))
        self.assertEqual(response_data.get('errcode'), 0)
        self.assertIsInstance(response_data.get('errmsg'), str)

    def test_login_with_invalid_credentials(self):
        """
        测试无效凭证的登录。
        """
        response = self.client.post(self.login_url, {'code': '12354'}, format='json')
        response_data = response.json()
        self.assertEqual(response_data.get('errcode'), 40029)  
        self.assertIsInstance(response_data.get('errmsg'), str)

    def test_login_with_wrong_method(self):
        """
        测试使用错误的请求方式。
        """
        response = self.client.get(self.login_url, {'code': '3e5428-ff58yj5'}, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), '405')
        self.assertEqual(response_data.get('message'), 'Method not allowed')

class SearchAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.search_url = reverse('search')  

    def test_search_with_valid_request(self):
        """
        测试有效请求的搜索。
        """
        response = self.client.post(self.search_url, {
            "openid": "88hrt-j37db-x56kt-fkyou",
            "searchWord": "a"
        }, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('info'), "Success in word searching")
        self.assertIsInstance(response_data.get('results'), list)

    def test_search_with_wrong_method(self):
        """
        测试使用错误的请求方式。
        """
        response = self.client.get(self.search_url, {
            "openid": "88hrt-j37db-x56kt-fkyou",
            "searchWord": "5"
        }, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), '405')
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_search_with_valid_request2(self):
        """
        测试有效请求的搜索。
        """
        response = self.client.post(self.search_url, {
            "openid": "88hrt-j37db-x56kt-fkyou",
            "searchWord": "aads"
        }, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('info'), "Success in word searching")
        self.assertIsInstance(response_data.get('results'), list)

class WordDetailAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.detail_url = reverse('detail')  

    def test_word_detail_with_valid_request(self):
        """
        测试有效请求的单词详情获取。
        """
        response = self.client.post(self.detail_url, {
            "openid": "dskadhkskada",
            "word":"赤い【あかい◎】",
        }, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('info'), "Success in word searching")
        detail = response_data.get('detail')
        self.assertIsNotNone(detail)
        self.assertEqual(detail.get('name'),"赤い【あかい◎】")
        self.assertEqual(detail.get('accent'),0)
        self.assertEqual(detail.get('kana'),["あ","か","い"])
        self.assertEqual(detail.get('taka'),[0,1,1])
        self.assertEqual(detail.get('wave'),[0,1,1])
        self.assertEqual(detail.get('type'),"形")
        self.assertIsNotNone(detail.get('exsent'))

    def test_word_detail_with_wrong_method(self):
        """
        测试使用错误的请求方式获取单词详情。
        """
        response = self.client.get(self.detail_url, {
            "openid": "dskadhkskada",
            "word": "赤い&#8203;``【oaicite:0】``&#8203;"
        }, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), '405')
        self.assertEqual(response_data.get('message'), "Method not allowed")

    # def test_word_detail_with_valid_request2(self):
    #     """
    #     测试有效请求的单词详情获取。
    #     """
    #     response = self.client.post(self.detail_url, {
    #         "openid": "dskadhkskada",
    #         "word":"赤い",
    #     }, format='json')
    #     response_data = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_data.get('code'), 0)
    #     self.assertEqual(response_data.get('info'), "Success in word searching")
    #     detail = response_data.get('detail')
    #     self.assertIsNotNone(detail)
    
class ListAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.list_url = reverse('list') 

    def test_list_with_valid_request(self):
        """
        测试有效请求的训练队列获取。
        """
        response = self.client.post(self.list_url, {
            "openid": "3e5428-ff58yj5",
            "type": 2  # 使用一个有效的类型值
        }, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('info'), "Success in word searching")
        medicine = response_data.get('medicine')
        self.assertIsInstance(medicine, list)


    def test_list_with_wrong_method(self):
        """
        测试使用错误的请求方式获取训练队列。
        """
        response = self.client.get(self.list_url, {
            "openid": "dskadhkskada",
            "type": 2
        }, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), '405')
        self.assertEqual(response_data.get('message'), "Method not allowed")

from django.core.files.uploadedfile import SimpleUploadedFile

class ReadAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.read_url = reverse('read')  

    # def test_read_with_valid_request(self):
    #     """
    #     测试有效请求的发音评测。
    #     """
    #     mock_audio_file = SimpleUploadedFile("word.mp3", b"010101011111", content_type="audio/mpeg")
    #     response = self.client.post(self.read_url, {
    #         "openid": "dskadhkskada",
    #         "file": mock_audio_file,
    #         "wave": [0, 1, 1, 0],
    #         "word": "赤い【あかい◎】" 
    #     }, format='mutipart')
    #     response_data = response.json()
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response_data.get('code'), 0)
    #     self.assertEqual(response_data.get('info'), "Success in word analyzing")
    #     self.assertIsNotNone(response_data.get('accent'))

    def test_read_with_wrong_method(self):
        """
        测试使用错误的请求方式进行发音评测。
        """
        response = self.client.get(self.read_url, {
            "openid": "dskadhkskada",
            "file": ...,  
            "wave": [0, 1, 1, 0],
            "word": "赤い【あかい◎】" 
        }, format='multipart')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), '405')
        self.assertEqual(response_data.get('message'), "Method not allowed")

class HeadIconAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.headicon_url = reverse('getlogheadicon')  

    def test_headicon_with_valid_openid(self):
        """
        测试使用有效openid获取头像。
        """
        data = {'openid': '3e5428-ff58yj5'}
        response = self.client.post(self.headicon_url, json.dumps(data), content_type="application/json")
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('headicon', response_data)

    def test_headicon_with_invalid_openid(self):
        """
        测试使用无效openid获取头像。
        """
        data = {'openid': 'invalid_openid'}
        response = self.client.post(self.headicon_url, json.dumps(data), content_type="application/json")
        response_data = response.json()
        self.assertEqual(response.status_code, 401)
        self.assertNotIn('headicon', response_data)

    def test_headicon_with_wrong_method(self):
        """
        测试使用错误的请求方式。
        """
        data = {'openid': '3e5428-ff58yj5'}
        response = self.client.get(self.headicon_url, data)
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

class HeadIconAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.headicon_url = reverse('headicon_change')  

    def test_headicon_with_valid_request(self):
        """
        测试使用有效请求更改头像。
        """
        mock_file = SimpleUploadedFile("test.jpg", b"file_content", content_type="image/jpeg")
        valid_data = {"openid": "3e5428-ff58yj5", "file": mock_file, "name": "test.jpg"}
        response = self.client.post(self.headicon_url, valid_data, format='multipart')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Headicon successfully changed!")

    def test_headicon_with_wrong_method(self):
        """
        测试使用错误的请求方式更改头像。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "file": ..., "name": "test.jpg"}
        response = self.client.get(self.headicon_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_headicon_with_invalid_user(self):
        """
        测试使用不存在用户更改头像。
        """
        invalid_user_data = {"openid": "invalid_user", "file": ..., "name": "test.jpg"}
        response = self.client.post(self.headicon_url, invalid_user_data, format='multipart')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

class NicknameAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.nickname_url = reverse('nickname_change')  

    def test_nickname_change_with_valid_request(self):
        """
        测试使用有效请求更改昵称。
        """
        valid_data = {"openid": "3e5428-ff58yj5", "nickname": "new_nickname"}
        response = self.client.post(self.nickname_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Nickname successfully changed!")

    def test_nickname_change_with_wrong_method(self):
        """
        测试使用错误的请求方式更改昵称。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "nickname": "new_nickname"}
        response = self.client.get(self.nickname_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_nickname_change_with_invalid_user(self):
        """
        测试使用不存在用户更改昵称。
        """
        invalid_user_data = {"openid": "invalid_user", "nickname": "new_nickname"}
        response = self.client.post(self.nickname_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

class TimelineAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.timeline_url = reverse('timeline_change')  

    def test_timeline_change_with_valid_request(self):
        """
        测试使用有效请求更改时间线。
        """
        valid_data = {"openid": "3e5428-ff58yj5", "timeline": 12}
        response = self.client.post(self.timeline_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Timeline successfully changed!")

    def test_timeline_change_with_wrong_method(self):
        """
        测试使用错误的请求方式更改时间线。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "timeline": 12}
        response = self.client.get(self.timeline_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_timeline_change_with_invalid_user(self):
        """
        测试使用不存在的用户更改时间线。
        """
        invalid_user_data = {"openid": "invalid_user", "timeline": 12}
        response = self.client.post(self.timeline_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

class RecordAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.record_url = reverse('record_change') 

    def test_record_change_with_valid_request(self):
        """
        测试使用有效请求更改记录按钮状态。
        """
        valid_data = {"openid": "3e5428-ff58yj5", "recordOn": "false"}
        response = self.client.post(self.record_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Record button successfully changed!")

    def test_record_change_with_wrong_method(self):
        """
        测试使用错误的请求方式更改记录按钮状态。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "recordOn": "false"}
        response = self.client.get(self.record_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_record_change_with_invalid_user(self):
        """
        测试使用不存在的用户更改记录按钮状态。
        """
        invalid_user_data = {"openid": "invalid_user", "recordOn": "false"}
        response = self.client.post(self.record_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

class WordbookCreateAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.create_wordbook_url = reverse('wb_create')  

    def test_create_wordbook_with_valid_request(self):
        """
        测试使用有效请求创建单词本。
        """
        valid_data = {"openid": "3e5428-ff58yj5"}
        response = self.client.post(self.create_wordbook_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "New wordbook successfully created!")

    def test_create_wordbook_with_wrong_method(self):
        """
        测试使用错误的请求方式创建单词本。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5"}
        response = self.client.get(self.create_wordbook_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_create_wordbook_with_invalid_user(self):
        """
        测试使用不存在的用户创建单词本。
        """
        invalid_user_data = {"openid": "invalid_user"}
        response = self.client.post(self.create_wordbook_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

class WordbookTypeChangeAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.change_type_url = reverse('wb_type')  

    def test_change_wordbook_type_with_valid_request(self):
        """
        测试使用有效请求更改单词本公开属性。
        """
        valid_data = {"openid": "3e5428-ff58yj5", "index": 2, "type": 0}
        response = self.client.post(self.change_type_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Wordbook information successfully changed!")

    def test_change_wordbook_type_with_wrong_method(self):
        """
        测试使用错误的请求方式更改单词本公开属性。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "index": 2, "type": 0}
        response = self.client.get(self.change_type_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_change_wordbook_type_with_invalid_user(self):
        """
        测试使用不存在的用户更改单词本公开属性。
        """
        invalid_user_data = {"openid": "invalid_user", "index": 2, "type": 0}
        response = self.client.post(self.change_type_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

    def test_change_wordbook_type_with_nonexistent_wordbook(self):
        """
        测试更改不存在的单词本公开属性。
        """
        nonexistent_wordbook_data = {"openid": "3e5428-ff58yj5", "index": 999, "type": 0}
        response = self.client.post(self.change_type_url, nonexistent_wordbook_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data.get('code'), "404")
        self.assertEqual(response_data.get('message'), "Wordbook not found")

class WordbookRemoveAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.remove_wordbook_url = reverse('wb_remove')  

    def test_remove_wordbook_with_valid_request(self):
        """
        测试使用有效请求删除单词本。
        """
        valid_data = {"openid": "3e5428-ff58yj5", "index": 2}
        response = self.client.post(self.remove_wordbook_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Wordbook removed successfully!")

    def test_remove_wordbook_with_wrong_method(self):
        """
        测试使用错误的请求方式删除单词本。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "index": 2}
        response = self.client.get(self.remove_wordbook_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_remove_wordbook_with_invalid_user(self):
        """
        测试使用不存在的用户删除单词本。
        """
        invalid_user_data = {"openid": "invalid_user", "index": 2}
        response = self.client.post(self.remove_wordbook_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

    def test_remove_wordbook_with_nonexistent_wordbook(self):
        """
        测试删除不存在的单词本。
        """
        nonexistent_wordbook_data = {"openid": "3e5428-ff58yj5", "index": 999}
        response = self.client.post(self.remove_wordbook_url, nonexistent_wordbook_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data.get('code'), "404")
        self.assertEqual(response_data.get('message'), "Wordbook not found")

class WordAddAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.add_word_url = reverse('word_add')  

    def test_add_word_with_valid_request(self):
        """
        测试使用有效请求添加单词到单词本。
        """
        valid_data = {"openid": "xxxx", "index": 2, "word": "あかい…"}
        response = self.client.post(self.add_word_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn(response_data.get('code'), [0])
        self.assertIn(response_data.get('message'), ["Word added successfully!", "Word already exists"])

    def test_add_word_with_wrong_method(self):
        """
        测试使用错误的请求方式添加单词到单词本。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "index": 2, "word": "あかい…"}
        response = self.client.get(self.add_word_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_add_word_with_invalid_user(self):
        """
        测试使用不存在的用户添加单词到单词本。
        """
        invalid_user_data = {"openid": "invalid_user", "index": 2, "word": "あかい…"}
        response = self.client.post(self.add_word_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

    def test_add_word_to_nonexistent_wordbook(self):
        """
        测试添加单词到不存在的单词本。
        """
        nonexistent_wordbook_data = {"openid": "3e5428-ff58yj5", "index": 999, "word": "あかい…"}
        response = self.client.post(self.add_word_url, nonexistent_wordbook_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data.get('code'), "404")
        self.assertEqual(response_data.get('message'), "Wordbook not found")

class WordRemoveAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.remove_word_url = reverse('remove_word')  

    def test_remove_word_with_valid_request(self):
        """
        测试使用有效请求从单词本中删除单词。
        """
        valid_data = {"openid": "xxxx", "index": 2, "word": "あかい…"}
        response = self.client.post(self.remove_word_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Word removed successfully!")

    def test_remove_word_with_wrong_method(self):
        """
        测试使用错误的请求方式从单词本中删除单词。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "index": 2, "word": "あかい…"}
        response = self.client.get(self.remove_word_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_remove_word_with_invalid_user(self):
        """
        测试使用不存在的用户从单词本中删除单词。
        """
        invalid_user_data = {"openid": "invalid_user", "index": 2, "word": "あかい…"}
        response = self.client.post(self.remove_word_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

    def test_remove_word_from_nonexistent_wordbook(self):
        """
        测试从不存在的单词本中删除单词。
        """
        nonexistent_wordbook_data = {"openid": "3e5428-ff58yj5", "index": 999, "word": "あかい…"}
        response = self.client.post(self.remove_word_url, nonexistent_wordbook_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data.get('code'), "404")
        self.assertEqual(response_data.get('message'), "Wordbook not found")

    def test_remove_nonexistent_word(self):
        """
        测试删除不存在的单词。
        """
        nonexistent_word_data = {"openid": "3e5428-ff58yj5", "index": 2, "word": "不存在的单词"}
        response = self.client.post(self.remove_word_url, nonexistent_word_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response_data.get('code'), "404")
        self.assertEqual(response_data.get('message'), "Word doesn't exist")


class FriendsListAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.friends_list_url = reverse('friends_list')  

    def test_get_friends_list_with_valid_request(self):
        """
        测试使用有效请求获取关注的用户信息列表。
        """
        valid_data = {"openid": "3e5428-ff58yj5"}
        response = self.client.post(self.friends_list_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertIsInstance(response_data.get('data').get('result'), list)

    def test_get_friends_list_with_wrong_method(self):
        """
        测试使用错误的请求方式获取关注的用户信息列表。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5"}
        response = self.client.get(self.friends_list_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_get_friends_list_with_invalid_user(self):
        """
        测试使用不存在的用户获取关注的用户信息列表。
        """
        invalid_user_data = {"openid": "invalid_user"}
        response = self.client.post(self.friends_list_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

class FriendsHeadIconAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.headicon_url = reverse('friends_headicon')  

    def test_get_headicon_with_valid_request(self):
        """
        测试使用有效请求通过uid获取用户头像。
        """
        valid_data = {"openid": "3e5428-ff58yj5", "uid": "10000001"}
        response = self.client.post(self.headicon_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)

    def test_get_headicon_with_wrong_method(self):
        """
        测试使用错误的请求方式获取用户头像。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "uid": "10000001"}
        response = self.client.get(self.headicon_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_get_headicon_with_invalid_user(self):
        """
        测试使用不存在的用户获取头像。
        """
        invalid_user_data = {"openid": "11", "uid": "10000001"}
        response = self.client.post(self.headicon_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

class FriendsFollowAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.follow_url = reverse('friends_follow')  

    def test_follow_with_valid_request(self):
        """
        测试使用有效请求通过uid关注用户。
        """
        valid_data = {"openid": "3e5428-ff58yj5", "uid": "10000001"}
        response = self.client.post(self.follow_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "successfully follow")

    def test_follow_with_wrong_method(self):
        """
        测试使用错误的请求方式关注用户。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "uid": "10000001"}
        response = self.client.get(self.follow_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_follow_with_invalid_user(self):
        """
        测试使用不存在的用户进行关注。
        """
        invalid_user_data = {"openid": "3ef58yj5", "uid": "10000001"}
        response = self.client.post(self.follow_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

class FriendsUnfollowAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.unfollow_url = reverse('friends_unfollow') 

    def test_unfollow_with_valid_request(self):
        """
        测试使用有效请求通过uid取消关注用户。
        """
        valid_data = {"openid": "3e5428-ff58yj5", "uid": "10000001"}
        response = self.client.post(self.unfollow_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "successfully unfollow")

    def test_unfollow_with_wrong_method(self):
        """
        测试使用错误的请求方式取消关注用户。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "uid": "10000001"}
        response = self.client.get(self.unfollow_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_unfollow_with_invalid_user(self):
        """
        测试使用不存在的用户进行取消关注。
        """
        invalid_user_data = {"openid": "3e5428 ", "uid": "10000001"}
        response = self.client.post(self.unfollow_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

class FriendsUidSearchAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.uidsearch_url = reverse('friends_uidsearch')  

    def test_uidsearch_with_valid_request(self):
        """
        测试使用有效请求通过uid搜索用户。
        """
        valid_data = {"openid": "3e5428-ff58yj5 ", "uid": "10000001"}
        response = self.client.post(self.uidsearch_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertIsInstance(response_data.get('data').get('result'), list)

    def test_uidsearch_with_wrong_method(self):
        """
        测试使用错误的请求方式搜索用户。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "uid": "10000001"}
        response = self.client.get(self.uidsearch_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_uidsearch_with_invalid_user(self):
        """
        测试使用不存在的用户进行搜索。
        """
        invalid_user_data = {"openid": "ff", "uid": "10000001"}
        response = self.client.post(self.uidsearch_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")

class FriendsNameSearchAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.namesearch_url = reverse('friends_namesearch') 

    def test_namesearch_with_valid_request(self):
        """
        测试使用有效请求通过昵称搜索用户。
        """
        valid_data = {"openid": "3e5428-ff58yj5", "name": "萝莉控"}
        response = self.client.post(self.namesearch_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertIsInstance(response_data.get('data').get('result'), list)

    def test_namesearch_with_wrong_method(self):
        """
        测试使用错误的请求方式搜索用户。
        """
        wrong_method_data = {"openid": "3e5428-ff58yj5", "name": "萝莉控"}
        response = self.client.get(self.namesearch_url, wrong_method_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        self.assertEqual(response_data.get('code'), "405")
        self.assertEqual(response_data.get('message'), "Method not allowed")

    def test_namesearch_with_invalid_user(self):
        """
        测试使用不存在的用户进行搜索。
        """
        invalid_user_data = {"openid": "ss", "name": "萝莉控"}
        response = self.client.post(self.namesearch_url, invalid_user_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response_data.get('code'), "401")
        self.assertEqual(response_data.get('message'), "User Unauthorized")