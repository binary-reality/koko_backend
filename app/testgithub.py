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