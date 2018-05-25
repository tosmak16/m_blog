from django.test import TestCase, Client
import json

client = Client()


class QuickApiTest(TestCase):
    user_data = {'email': 'tosmak16@gmail.com', 'username': 'tosmak', 'password': '1234asdf'}

    def test_user_register_successfully(self):

        response = self.client.post('/users/signup/', data= self.user_data)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(json_response.get('message'), 'you have logged in successfully')
        self.assertIsNotNone(json_response.get('token'))

    def test_user_registration_failed_when_email_is_empty(self):
        self.user_data.update({'email': ''})
        response = self.client.post('/users/signup/', data= self.user_data)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response.get('message').get('email'), ['This field may not be blank.'])
        self.assertIsNone(json_response.get('token'))

    def test_user_can_not_create_an_already_existing_email(self):

        self.client.post('/users/signup/', data=self.user_data)
        response = self.client.post('/users/signup/', data=self.user_data)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(json_response.get('message').get('username'), ['user with this username already exists.'])
        self.assertIsNone(json_response.get('token'))

    def test_user_login_sucessfully(self):
        self.client.post('/users/signup/', data= self.user_data)

        response = self.client.post('/users/signin/', data=self.user_data)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(json_response.get('message'), 'you have logged in successfully')
        self.assertIsNotNone(json_response.get('token'))

    def test_user_login_not_sucessful_when_user_data_does_not_exist(self):

        response = self.client.post('/users/signin/', data=self.user_data)
        json_response = json.loads(response.content)
        self.assertEqual(response.status_code, 401)
        self.assertEqual(json_response.get('message'), 'email and password is incorrect')
        self.assertIsNone(json_response.get('token'))











