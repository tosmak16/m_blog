
from django.test import TestCase, Client

client = Client()


class QuickApiTest(TestCase):

    def test_index_view_returns_a_response_message(self):
        """
        checks if index_view returns a response
        message when get request is sent
        """

        response = client.get('/')

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content, b'Hello welcome to my blog')

