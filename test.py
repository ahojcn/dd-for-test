import unittest
import requests
import json


# 基本功能测试，全部参数
class TestBase(unittest.TestCase):

    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8383/DD'
        self.headers = {'Content-Type': 'application/json'}
        self.data = {'Name': 'ahojcn', 'Height': 175,
                     'Weight': 85, 'Gender': 'male',
                     'Age': 21, 'Email': 'ahojcn@qq.com'}

    # 基本响应测试
    def test_base_01(self):
        s = requests.session()
        r = s.post(url=self.url, headers=self.headers, data=json.dumps(self.data))
        result = r.json()

        # check
        self.assertEqual(r.status_code, 200)
        self.assertEqual(result['status'], 0)
        self.assertEqual(result['message'], 'ok')
        self.assertEqual(result['data'], self.data)

    # 测试 URL 路径
    def test_base_02(self):
        url = 'http://127.0.0.1:8383/dd'
        s = requests.session()
        r = s.post(url=url, headers=self.headers, data=json.dumps(self.data))

        # check
        self.assertEqual(r.status_code, 404)


# 参数相关测试
class TestParams(unittest.TestCase):

    def setUp(self) -> None:
        self.url = 'http://127.0.0.1:8383/DD'
        self.headers = {'Content-Type': 'application/json'}
        self.data = {'Name': 'ahojcn', 'Height': 175,
                     'Weight': 85, 'Gender': 'male',
                     'Age': 21, 'Email': 'ahojcn@qq.com'}

    # 没有传递参数
    def test_no_params(self):
        s = requests.session()
        r = s.post(url=self.url, headers=self.headers)
        result = r.json()

        # check
        self.assertEqual(result['status'], -2)
        self.assertEqual(result['message'], 'params error')
        self.assertEqual(result['data'], None)

    # 整体参数类型错误
    def test_params_type_error(self):
        s = requests.session()
        r = s.post(url=self.url, headers=self.headers, data={})
        result = r.json()

        # check
        self.assertEqual(result['status'], -2)
        self.assertEqual(result['message'], 'params error')
        self.assertEqual(result['data'], None)

    # 传递一个不存在的 key
    def test_params_not_exits(self):
        s = requests.session()
        data = {'Name': 'ahojcn', 'Height': 175,
                'Weight': 85, 'Gender': 'male',
                'Age': 21, 'Email': 'ahojcn@qq.com',
                'TestKey': 'TestKey'}
        r = s.post(url=self.url, headers=self.headers, data=json.dumps(data))
        result = r.json()

        # check
        self.assertEqual(result['status'], 0)
        self.assertEqual(result['message'], 'ok')
        self.assertEqual(result['data'], self.data)

    # 测试非法字符
    def test_params_illegal_char(self):
        s = requests.session()
        data = {'Name': '≈¬åßååç≈çœ∑￿π', 'Height': 175,
                'Weight': 85, 'Gender': 'male',
                'Age': 21, 'Email': 'ahojcn@qq.com'}
        r = s.post(url=self.url, headers=self.headers, data=json.dumps(data))
        result = r.json()

        # check
        self.assertEqual(result['status'], 0)
        self.assertEqual(result['message'], 'ok')
        self.assertEqual(result['data'], data)

    # 传递所有参数为空
    def test_params_no_reference_all(self):
        s = requests.session()
        data = {}
        r = s.post(url=self.url, headers=self.headers, data=json.dumps(data))
        result = r.json()

        # check
        self.assertEqual(result['status'], -1)
        self.assertEqual(result['message'], 'Name should be betwween 2 and 20 chars long')
        self.assertEqual(result['data'], {'Name': '', 'Height': 0, 'Weight': 0, 'Gender': '', 'Age': 0, 'Email': ''})

    # 缺少一个必填项 Email
    def test_params_no_reference_one(self):
        s = requests.session()
        data = {'Name': 'ahojcn', 'Height': 175,
                'Weight': 85, 'Gender': 'male', 'Age': 21}
        r = s.post(url=self.url, headers=self.headers, data=json.dumps(data))
        result = r.json()

        # check
        self.assertEqual(result['status'], -1)
        self.assertEqual(result['message'], 'Email is not a email address')
        data['Email'] = ''
        self.assertEqual(result['data'], data)

    # 参数越界 Gender in ['male', 'female', 'secret']
    def test_params_cross_border(self):
        data = {'Name': 'ahojcn', 'Height': 175,
                'Weight': 85, 'Gender': 'xxx',
                'Age': 21, 'Email': 'ahojcn@qq.com'}
        s = requests.session()
        r = s.post(url=self.url, headers=self.headers, data=json.dumps(data))
        result = r.json()

        # check
        self.assertEqual(result['status'], -1)
        self.assertEqual(result['message'], 'Gender is not in params [male female secret]')
        self.assertEqual(result['data'], data)

    # 参数类型 Weight is number, test string
    def test_params_type(self):
        data = {'Name': 'ahojcn', 'Height': 175,
                'Weight': '85', 'Gender': 'secret',
                'Age': 21, 'Email': 'ahojcn@qq.com'}
        s = requests.session()
        r = s.post(url=self.url, headers=self.headers, data=json.dumps(data))
        result = r.json()

        # check
        self.assertEqual(result['status'], -2)
        self.assertEqual(result['message'], 'params error')
        self.assertEqual(result['data'], None)

    # 参数边界测试
    def test_params_border(self):
        data = {'Name': 'ah', 'Height': 175,
                'Weight': 85, 'Gender': 'secret',
                'Age': 21, 'Email': 'ahojcn@qq.com'}
        s = requests.session()
        r = s.post(url=self.url, headers=self.headers, data=json.dumps(data))
        result = r.json()

        print(result)

        # check
        self.assertEqual(result['status'], 0)
        self.assertEqual(result['message'], 'ok')
        self.assertEqual(result['data'], data)


if __name__ == '__main__':
    unittest.main()
