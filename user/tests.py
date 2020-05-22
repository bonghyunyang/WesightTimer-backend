import json
import bcrypt
import jwt

from django.test      import TestCase, Client
from wesight.settings import SECRET_KEY
from user.models      import User

class SignUpTest(TestCase):

    def setUp(self):
        User.objects.create(
           email             = "bbbb@bbbb.com",
           full_name         = "aaa",
           password          = "qqqqqq111"
        )

    def tearDown(self):
        User.objects.all().delete()
    
    def test_signup_bed_password(self):
        client = Client()
        sign_user = {
            "email" : "sqqqqq@naver.com",
            "full_name": "sdfasfsafsadf",
            "password" : "12q1"
        }
        response = client.post('/user/signup', json.dumps(sign_user), content_type='application/json')
        self.assertEquals(response.status_code, 400)
    
    def test_signup_value_error1(self):
        client = Client()
        sign_user = {
            "email" : "",
            "full_name": "nam gung minsu",
            "password" : "dfsf555sdf"
        }
        response = client.post('/user/signup', json.dumps(sign_user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_signup_value_error2(self):
        client = Client()
        sign_user = {
            "email" : "sdfsafasf",
            "password" : "dfsf555sdf"
        }
        response = client.post('/user/signup', json.dumps(sign_user), content_type='application/json')
        self.assertEqual(response.status_code, 400)

    def test_signup_value_key_error(self):
        client = Client()
        sign_user = {
            "email" : "sdfsafasf",
            "name": "sdfasfaf",
            "password" : "dfsf555sdf"
        }
        response = client.post('/user/signup', json.dumps(sign_user), content_type='application/json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(),
        {'MESSAGE':'INVALIED_KEY'})

    def test_signup_value_success(self):
        client = Client()
        sign_user = {
            "email" : "dddeffw@naver.com",
            "full_name": "sdfasfaf",
            "password" : "dfsf555sdf"
        }
        response = client.post('/user/signup', json.dumps(sign_user), content_type='application/json')
        self.assertEqual(response.status_code, 200)

    def test_signup_exsist_user(self):
        client = Client()
        sign_user = {
            "email" : "bbbb@bbbb.com",
            "full_name": "nam gung minsu",
            "password" : "dsd050505f"
        }
        response = client.post('/user/signup', json.dumps(sign_user), content_type='application/json')
        self.assertEqual(response.status_code, 401) 
        self.assertEqual(response.json(),
            {'MESSAGE' : 'ALREADY_EXSIST'})

class SignInTest(TestCase):

    def setUp(self):
        User.objects.create(
           email             = "bbbb@bbbb.com",
           full_name         = "aaa",
           password          = bcrypt.hashpw("aaa123".encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        )

    def tearDown(self):
        User.objects.all().delete()

    def test_user_login_email_does_not_exist(self):
        client = Client()
        loguloguin = {
           "email"      : "asdf@basdff.com",
           "password"   : "aaa123"
        }
        response = client.post('/user/signin', json.dumps(loguloguin), content_type='application/json')
        self.assertEqual(response.status_code, 401)
    
    def test_user_login_wrong_password(self):
        client = Client()
        loguloguin = {
           "email"      : "bbbb@bbbb.com",
           "password"   : "sdfsfsfsfssfsfs"
        }
        response = client.post('/user/signin', json.dumps(loguloguin), content_type='application/json')
        self.assertEqual(response.status_code, 401)
    
    def test_user_login_wrong_key(self):
        client = Client()
        loguloguin = {
           "email"      : "bbbb@bbbb.com",
           "sdsffs"   : "sdfsfsfsfssfsfs"
        }
        response = client.post('/user/signin', json.dumps(loguloguin), content_type='application/json')
        self.assertEqual(response.status_code, 400)
    
    def test_user_success(self):
        client = Client()
        loguloguin = {
           "email"    : "bbbb@bbbb.com",
           "password"   : "aaa123"
        }
        user = User.objects.get(email = "bbbb@bbbb.com")
        response = client.post('/user/signin', json.dumps(loguloguin), content_type='application/json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(),
            {"token_issued" : jwt.encode({'id': user.id}, SECRET_KEY, algorithm='HS256').decode('utf-8'),
             "email": "bbbb@bbbb.com",
             "name" : "aaa"
            })


