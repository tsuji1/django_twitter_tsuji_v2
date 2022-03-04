from django.test import TestCase
from django.urls import reverse

class HomepageTests(TestCase):
    def setUp(self):
        self.response = self.client.get(reverse('twitter:homepage'))
    def test_successful_response(self):
        self.assertEqual(self.response.status_code, 200)
