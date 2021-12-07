from django.test import TestCase
from .tasks import *
import requests

class ViewsTestCase(TestCase):

    def test_home_page(self):    
        '''Home Page Testing'''      
        print("\n -> Testing Home Page ( GET )")

        # GET request -> 200
        get_resp = requests.get('http://127.0.0.1:8000/')
        self.assertEqual(get_resp.status_code, 200)


    def test_login_page(self):          
        '''Login Page Testing'''      
        print("\n -> Testing Login Page (GET / POST)")
        
        # GET request -> 200
        get_resp = requests.get('http://127.0.0.1:8000/login/')
        self.assertEqual(get_resp.status_code, 200)

        # POST request
        cookies = get_resp.cookies.get_dict()
        post_resp = requests.post(url='http://127.0.0.1:8000/login/',data={'username': 'adwait', 'password': 'Testing@123', 'csrf_token':cookies['csrftoken']}, cookies=cookies)
        self.assertEqual(post_resp.status_code, 200)
        

    def test_dashboard_page(self):          
        '''Dashboard Page'''      
        print("\n -> Testing Dashboard Page (GET)")
        
        # without session Id (User not Loggedin)
        response = requests.get('http://127.0.0.1:8000/dashboard/',allow_redirects=False)
        self.assertEqual(response.status_code, 302)
        
        #  with a valid session Id (Society Member Loggedin)
        dashboard_resp = requests.get('http://127.0.0.1:8000/dashboard/',cookies={'sessionid':'7uomc3d4wo9w9rmhlhoukmyusenas42m'},allow_redirects=False)
        self.assertEqual(dashboard_resp.status_code, 200)

        #  with an invalid session Id 
        dashboard_resp = requests.get('http://127.0.0.1:8000/dashboard/',cookies={'sessionid':'7uomc3d4woBSEFlhoukmyusenas42m'},allow_redirects=False)
        self.assertEqual(dashboard_resp.status_code, 302)

    def test_mail(self):
        '''Send mail'''
        print("\n -> Testing test_mail() (function)")

        # Testing send_mail_func()
        resp = send_mail_func.delay()
        self.assertTrue(resp)

