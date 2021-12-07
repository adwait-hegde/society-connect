from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User

class ViewsTestCase(TestCase):

  
    # def test_index_loads_properly(self):
    #     """The index page loads properly"""
    #     print("hahaha")
    #     response = self.client.get('http://127.0.0.1:8000/')
    #     self.assertEqual(response.status_code, 200)

    def test_home_page_loads_properly(self):    
        '''Home Page'''      
        print(" -> Testing Home Page")
        response = self.client.get('http://127.0.0.1:8000/')
        self.assertEqual(response.status_code, 200)

    def test_login_page_loads_properly(self):          
        '''Login Page'''      
        print(" -> Testing Login Page (GET)")
        
        response = self.client.get('http://127.0.0.1:8000/login/')
        print(response)
        # print(response.headers['csrf_token'])
        self.assertEqual(response.status_code, 200)
        print("done with get now testing post")
        c = Client()
        csrf_client = Client(enforce_csrf_checks=True)
        # response = c.post('/login/', {'username': 'adwait', 'password': 'Testing@123','csrf_token':csrf_client})
        # print(response.headers)
        # print(response.url)
        # self.assertEqual(response.url, '/dashboard/')


        # login = self.client.login(username='adwait', password='Testing@123')
        # print(login)
        # response = self.client.post('http://127.0.0.1:8000/dashboard/')

        # Check that it lets us login - this is our book and we have the right permissions.
        # self.assertEqual(response.status_code, 200)
        response = c.post('/login/', {'username': 'adwait', 'password': 'Testing@123'})

        print(response.status_code)
        print(response.url)
        #        self.username = 'dummy' + data + '@gmail.com'
        # self.password = 'Dummy@123'
        # user = User.objects.create(username=self.username)
        # user.set_password(self.password)
        # user.save()
        # c = Client()
        # self.client_object = c.login(username=self.username, password=self.password)
        # self.content_type = "application/json"
        # response = self.client_object.post('/api/my-profile/', content_type=self.content_type)


    def test_dashboard_refuse_to_load(self):          
        '''Dashboard Page'''      
        print("dash")
        response = self.client.get('http://127.0.0.1:8000/dashboard')
        print(response.url)
        self.assertEqual(response.status_code, 301)

    
    # def test_pages_loads_properly(self):
    #     pages = ['','login/','dashboard']
    #     for page in pages:
    #         print("the page is",page)
    #         response = self.client.get('http://127.0.0.1:8000/'+page)
    #         self.assertEqual(response.status_code, 200)

    #     # pages = ['dashboard/']

    