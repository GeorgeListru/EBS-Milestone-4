from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient


# Create your tests here.


class TestUsers(TestCase):
    fixtures = ["users"]

    def setUp(self) -> None:
        self.client = APIClient()
        # check data in fixture json file
        self.test_user1 = User.objects.get(email="user1@email.com")

    def test_register(self):
        response = self.client.post(
            reverse("token_register"),
            {
                "first_name": "George",
                "last_name": "Listru",
                "email": "george@example.com",
                "password": "parola123"
            }
        )
        self.assertEqual(response.status_code, 200)
