from django.test import TestCase
from django.urls import reverse


class LoginViewTest(TestCase):
    def test_login_form_validation(self):
        response = self.client.post(reverse('login'), {'username': '', 'password': ''})
        self.assertContains(response, "This field is required")

        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpassword'})
        self.assertContains(response, "Invalid username or password")
