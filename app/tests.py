from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
import json

class LoginAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.login_url = reverse('login')  # 假设你在urls.py中命名你的登录视图为'login'

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
        self.assertEqual(response_data.get('errcode'), 40029)  # 替换some_error_code为具体的错误码
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
        self.search_url = reverse('search')  # 实际URL可能需要调整

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
        self.detail_url = reverse('detail')  # 实际URL可能需要调整

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
        self.list_url = reverse('list')  # 实际URL可能需要调整

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
        # 可以添加更多关于 medicine 列表内容的断言...

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
        self.read_url = reverse('read')   # 实际URL可能需要调整

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
            "file": ...,  # 这里的文件模拟可能需要根据实际情况调整
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
        self.headicon_url = reverse('getlogheadicon')  # 替换'headicon'为在urls.py中对应的name

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
        valid_data = {"openid": "dskadhkskada", "file": mock_file, "name": "test.jpg"}
        response = self.client.post(self.headicon_url, valid_data, format='multipart')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Headicon successfully changed!")

    def test_headicon_with_wrong_method(self):
        """
        测试使用错误的请求方式更改头像。
        """
        wrong_method_data = {"openid": "dskadhkskada", "file": ..., "name": "test.jpg"}
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
        valid_data = {"openid": "xxxx", "nickname": "new_nickname"}
        response = self.client.post(self.nickname_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Nickname successfully changed!")

    def test_nickname_change_with_wrong_method(self):
        """
        测试使用错误的请求方式更改昵称。
        """
        wrong_method_data = {"openid": "xxxx", "nickname": "new_nickname"}
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
        valid_data = {"openid": "xxxx", "timeline": 12}
        response = self.client.post(self.timeline_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Timeline successfully changed!")

    def test_timeline_change_with_wrong_method(self):
        """
        测试使用错误的请求方式更改时间线。
        """
        wrong_method_data = {"openid": "xxxx", "timeline": 12}
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
        self.record_url = reverse('record——change') 

    def test_record_change_with_valid_request(self):
        """
        测试使用有效请求更改记录按钮状态。
        """
        valid_data = {"openid": "xxxx", "recordOn": "false"}
        response = self.client.post(self.record_url, valid_data, format='json')
        response_data = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_data.get('code'), 0)
        self.assertEqual(response_data.get('message'), "Record button successfully changed!")

    def test_record_change_with_wrong_method(self):
        """
        测试使用错误的请求方式更改记录按钮状态。
        """
        wrong_method_data = {"openid": "xxxx", "recordOn": "false"}
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